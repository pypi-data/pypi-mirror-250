import multiprocessing
import time


import cobra
from cobra.flux_analysis.gapfilling import GapFiller
from cobra.util.solver import linear_reaction_coefficients



def get_objectives(model):
    """Get the IDs of the current objective reactions.
    
    Args:
        model (cobra.Model): target model.
        
    Returns:
        list: IDs of the reactions set as objective.

    """
    
    objs = list(linear_reaction_coefficients(model).keys())
    obj_ids = [obj.id for obj in objs]
    return obj_ids

        
        
def get_solver(model):
    """Get the ID of the solver associated to the model.
    
    Args:
        model (cobra.Model): target model.
        
    Returns:
        str: ID of the solver (for example: ``glpk_exact``).

    """
    
    solver = str(type(model.solver))
    solver = solver.replace('<class ', '')
    solver = solver.replace("'optlang.", '')
    solver = solver.replace("_interface.Model'>", '')
    
    return solver



def remove_rids(model, rids, inverse=False):
    """Remove reactions from the model given a list of reaction IDs.
    
    Args:
        model (cobra.Model): target model.
        rids (list): reaction IDs.
        inverse (bool): if ``True``, reactions IDs contained in `rids` will be the ones to keep and not to remove.

    """
    
    to_delete = []
    for r in model.reactions: 
        if not inverse:
            if r.id in rids:
                to_delete.append(r)
        else:
            if r.id not in rids:
                to_delete.append(r)
    universe.remove_reactions(to_delete)


        
def perform_gapfilling(model, universe, mid=None, slim=None, minflux=1.0, exr=False, nsol=3, solver='glpk'): 
    """Propose gap-filling solutions for the specified objective. 
    
    It's possible to gap-fill also for the biosynthesis of a specific metabolite.
    
    Args:
        model (cobra.Model): target model to gap-fill.
        universe (cobra.Model): model from which to take new reactions.
        mid (str): gap-fill for the biosynthesis of a specific metabolite having ID `mid`. Will be ignored if ``None``.
        slim (str): try to reduce the complexity of the universe, considering only its reactions carrying non-0 flux. Can be ``FBA`` or ``FVA``. Will be ignored if ``None``.
        minflux (float): minimal flux to grant through the objective reaction.
        nsol (int): number of alternative solutions. 
        solver (str): solver to use (usually ``glpk`` or ``cplex``).
        exr (bool): whether to allow the opening of new EX_change reactions.
        
    Returns:
        list: IDs of reactions proposed during the 1st solution.
    """
    
    
    # temporary changes (objective and solver are not modified)
    with model, universe: 


        # set new solver if needed (cannot be 'glpk_exact').
        if get_solver(model) != solver: model.solver = solver
        if get_solver(universe) != solver: universe.solver = solver


        # if focusing on a particular biosynthesis
        if mid != None:
            model.objective = add_demand(model, mid)
            universe.objective = add_demand(universe, mid)


        # if requested, try to reduce the universe complexity:
        if slim == 'FBA':
            fluxes = universe.optimize().fluxes
            rids_to_keep = fluxes[fluxes != 0].index
            remove_rids(universe, rids_to_keep, inverse=True)
        elif slim == 'FVA':
            fluxes = cobra.flux_analysis.flux_variability_analysis(universe, fraction_of_optimum=0.01, loopless=False)
            rids_to_keep = fluxes[(fluxes['minimum']!=0) | (fluxes['maximum']!=0)].index
            remove_rids(universe, rids_to_keep, inverse=True)


        # compute reactions to add.
        gapfiller = GapFiller(model, universe, 
            lower_bound = minflux,
            demand_reactions = False, 
            exchange_reactions = exr,
            integer_threshold = 1e-20,  
        )
        solutions = gapfiller.fill(iterations=nsol)


        # iterate the solutions:
        first_sol_rids = []  # rids proposed during the 1st solution
        verbose_string = ''
        for i, solution in enumerate(solutions):
            verbose_string = verbose_string + f'Solution {i+1}. Reactions to add: {len(solution)}.\n'


            # iterate the reactions: 
            counter = 0
            for r in solution: 
                counter += 1
                # Note: this 'r' is not linked to any model. 
                # Indeed, calling r.model, None will be returned. 
                verbose_string = verbose_string + f'{counter} {r.id} {r.name}\n'

                # populate results with IDs from first solution:
                if i == 0: first_sol_rids.append(r.id)


            # separate solutions with a new line:
            verbose_string = verbose_string + '\n'
        # print verbose output: 
        verbose_string = verbose_string.rstrip()
        print(verbose_string)
        return first_sol_rids
        
    

def get_universe(staining='neg'):
    """Return a CarveMe universe. 
    
    Args:
        staining (str): 'pos' or 'neg'.
        
    Returns: 
        cobra.Model: the selected universe.
    """
    
    # basically it's a wrapper of the recon function
    from gempipe.recon.networkrec import get_universe_template
    universe = get_universe_template(logger=None, staining=staining)
    
    return universe



def add_demand(model, mid):
    """Create a demand reaction, useful for debugging models.
    
    Args:
        model (cobra.Model): target model.
        mid (str): metabolite ID (compartment included) for which to create the demand.
        
    Returns:
        str: demand reaction ID.
    """
    
    rid = f"demand_{mid}"
    newr = cobra.Reaction(rid)
    model.add_reactions([newr])
    model.reactions.get_by_id(rid).reaction = f"{mid} -->"
    model.reactions.get_by_id(rid).bounds = (0, 1000)
    
    return rid



def can_synth(model, mid):
    """Check if the model can synthesize a given metabolite.
    
    Args:
        model (cobra.Model): target model.
        mid (str): metabolite ID (compartment included) for which to check the synthesis.
    
    Returns:
        (bool, float, str):
        
            `[0]` ``True`` if `mid` can be synthesized (``optimal`` status and positive flux).
        
            `[1]` maximal theoretical synthesis flux.
            
            `[2]` status of the optimizer.
    """
    
    # changes are temporary: demand is not added, objective is not changed.
    with model: 

        rid = add_demand(model, mid)

        # set the objective to this demand reaction:
        model.objective = rid

        # perform FBA: 
        res = model.optimize()
        value = res.objective_value
        status = res.status
        response = True if (value > 0 and status == 'optimal') else False
        
        return response, round(value, 2), status
    
    
    
def check_reactants(model, rid, verbose=True):
    """Check which reactant of a given reaction cannot be synthesized.
    
    Args:
        model (cobra.Model): target model.
        rid (str): reaction ID for which to check the synthesis of the reactants.
        verbose (bool): whether to print blocked reactants.
    
    Returns:
        list: IDs of blocked reactants.
    """
    
    # changes are temporary
    with model: 
        counter = 0

        
        # get reactants and products
        reacs = [m for m in model.reactions.get_by_id(rid).reactants]
        prods = [m for m in model.reactions.get_by_id(rid).products]

        
        # iterate through the reactants: 
        mid_blocked = []
        verbose_string = ''
        for m in reacs:
            
            # check if it can be synthesized:
            response, flux, status = can_synth(model, mid=m.id)
            
            if response==False: 
                counter += 1
                verbose_string = verbose_string + f'{counter} : {flux} : {status} : {m.id} : {m.name}\n'
                mid_blocked.append(m.id)

                
        verbose_string = verbose_string.rstrip()  # remove trailing endlines
        if verbose: print(verbose_string)
        return mid_blocked
    
    
    
def sensitivity_analysis(model, scaled=False, top=3, mid=None):
    """Perform a sensitivity analysis (or reduced costs analysis) focused on the EX_change reaction.
    
    It is based on the current model's objective. The returned dictionary is sorted from most negative to most positive values.
    
    Args:
        model (cobra.Model): target model.
        scaled (bool): whether to scale to the current objective value.
        top (int): get just the first and last `top` EX_change reactions. If ``None``, all EX_change reactions will be returned.
        mid (str): instead of optimizing for the current objective reaction, do the analysis on the biosynthesis of a specific metabolite having ID `mid`. If `None` it will be ignored.
    
    Returns:
        dict: reduced costs keyd by EX_change reaction ID. 
    """
    
    
    # temporary chenges:
    with model:
        
      
        # focus on a specific metbaolite
        if mid != None: 
            model.objective = add_demand(model, mid)


        res = model.optimize()
        obj = res.objective_value
        flx = res.fluxes.to_dict()
        rcs = res.reduced_costs.to_dict()


        # manage 0 flux exception:
        if obj == 0 and scaled == True:
            raise Exception("Cannot scale reduced costs id the objective value is 0")


        # get the reduced costs of the EXR only:
        rcsex = {} 
        for key in rcs:
            if key.startswith("EX_"):
                if not scaled : rcsex[key] = rcs[key]
                else: rcsex[key] = rcs[key] * flx[key] / obj


        # get the most impactful (lowest and highest)
        rcsex = sorted(rcsex.items(), key=lambda x: x[1], reverse=True)
        rcsex = {i[0]: i[1] for i in rcsex}  # convert list to dictionary
    
        
        # get only the top N and bottom N exchanges
        if top != None: 
            rcsex_filt = {}
            for i in range(top):
                rcsex_filt[ list(rcsex.keys())[i] ] = list(rcsex.values())[i]
            for i in range(top):
                rcsex_filt[ list(rcsex.keys())[-top +i] ] = list(rcsex.values())[-top +i]
            rcsex = rcsex_filt
        
        return rcsex
    
    
    
def query_pam(pam, annotation, panmodel, kos=[], names=[], egg=False, modeled=False):
    
    # create a copy to filter: 
    annotation_filter = annotation.copy()
    
    
    # filter for kegg orthologs
    if kos != []:
        good_clusters = []
        for ko in kos:
            good_clusters = good_clusters + list(annotation[annotation['KEGG_ko'].str.contains(f'ko:{ko}')].index)
        annotation_filter = annotation_filter.loc[good_clusters, ]
    
    
    # filter for kegg orthologs
    if names != []:
        good_clusters = []
        for name in names:
            good_clusters = good_clusters + list(annotation[annotation['Preferred_name'].str.contains(f'{name.lower()}', case=False)].index)
        annotation_filter = annotation.loc[good_clusters, ]
    
    
    # get tabular results (PAM or annotation)
    if egg: results = annotation_filter
    else: results = pam.loc[[i for i in annotation_filter.index if i in pam.index], ]
    
    
    # mark clusters that are already modeled:
    if modeled: 
        results_columns = list(results.columns)
        results['modeled'] = False
        for cluster in results.index:
            if cluster in [g.id for g in panmodel.genes]:
                results.loc[cluster, 'modeled'] = True
        results = results[['modeled'] + results_columns]  # reorder columns
    
    
    return results



def import_from_universe(model, universe, rid, bounds=None, gpr=None):

    
    r = universe.reactions.get_by_id(rid)
    model.add_reactions([r])
    
    if bounds != None:
        model.reactions.get_by_id(rid).bounds = bounds
        
    if gpr != None:
        model.reactions.get_by_id(rid).gene_reaction_rule = gpr
        model.reactions.get_by_id(rid).update_genes_from_gpr()
    