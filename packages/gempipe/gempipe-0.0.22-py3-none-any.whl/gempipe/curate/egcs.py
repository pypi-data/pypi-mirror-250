import re


import cobra





def close_boundaries(model):
    """Set all the EX_change reactions to (0, 0).
    
    Args:
        model (cobra.Model): target model.

    """
    
    for r in model.reactions:
        if len(r.metabolites)==1 and r.id.startswith('EX_'):
            r.bounds = (0, 0)



def verify_egc(model, mid, escher=False): 
    """Test the presence of energy-generating cycles (EGCs). 
    
    Can also output a model for Escher, with just the reactions composing the cycle. 
    
    Args:
        model (cobra.Model): target model. Must be encoded with the BiGG notation.
        mid (str): metabolite ID for which the EGC must be checked. Warning: must be without compartment, so for example ``atp`` instead of ``atp_c``. 
        escher (bool): save a reduced ``cobra.Model`` in the current directory. To be loaded in Escher. 

    """
    
    # changes as not permament: 
    with model: 
        
        # close all the exchange reactions: 
        close_boundaries(model)

                
        # create a dissipation reaction: 
        dissip = cobra.Reaction(f'__dissip__{mid}')
        model.add_reactions([dissip])
        dissip = model.reactions.get_by_id(f'__dissip__{mid}')
        
        
        # define the dissipation reaction:
        modeled_mids = [m.id for m in model.metabolites]
        if mid == 'atp':
            dissip_string = 'atp_c + h2o_c --> adp_c + pi_c + h_c'
        elif mid == 'ctp':
            dissip_string = 'ctp_c + h2o_c --> cdp_c + pi_c + h_c'
        elif mid == 'gtp':
            dissip_string = 'gtp_c + h2o_c --> gdp_c + pi_c + h_c'
        elif mid == 'utp':
            dissip_string = 'utp_c + h2o_c --> udp_c + pi_c + h_c'
        elif mid == 'itp':
            dissip_string = 'itp_c + h2o_c --> idp_c + pi_c + h_c'
        elif mid == 'nadh':
            dissip_string = 'nadh_c --> nad_c + h_c'
        elif mid == 'nadph':
            dissip_string = 'nadph_c --> nadp_c + h_c'
        elif mid == 'fadh2':
            dissip_string = 'fadh2_c --> fad_c + 2.0 h_c'
        elif mid == 'accoa':
            dissip_string = 'accoa_c + h2o_c --> ac_c + coa_c + h_c'
        elif mid == 'glu__L':
            if 'nh4_c' in modeled_mids :
                dissip_string = 'glu__L_c + h2o_c --> akg_c + nh4_c + 2.0 h_c'
            elif 'nh3_c' in modeled_mids :
                dissip_string = 'glu__L_c + h2o_c --> akg_c + nh3_c + 3.0 h_c'
            else:
                raise Exception("'nh4_c' or 'nh3_c' must be present in the model.")
        elif mid == 'q8h2':
            dissip_string = 'q8h2_c --> q8_c + 2.0 h_c'

        else: 
            raise Exception("Metabolite ID (mid) not recognized.") 
        dissip.build_reaction_from_string(dissip_string)
        
        
        # set the objective and optimize: 
        model.objective = f'__dissip__{mid}'
        res = model.optimize()
        
        
        # log some messages
        print(dissip.reaction)
        print( res.objective_value, ':', res.status )
    
    
        # get suspect !=0 fluxes (if any)
        if res.objective_value != 0: 
            fluxes = res.fluxes
            print()  # skip a line befor printing the EGC members
            
            # get interesting fluxes (0.001 tries to take into account the approximation in glpk and cplex solvers)
            fluxes_interesting = fluxes[((fluxes > 0.001) | (fluxes < -0.001)) & (fluxes.index != f'__dissip__{mid}')]
            print(fluxes_interesting.to_string())
            
            
            # create a model for escher
            if escher:  
                model_copy = model.copy()
                all_rids = [r.id for r in model_copy.reactions]
                to_delete = set(all_rids) - set(fluxes_interesting.index)
                model_copy.remove_reactions(to_delete)
                cobra.io.save_json_model(model_copy, f'__dissip__{mid}' + '.json')
                print(f'__dissip__{mid}' + '.json', "saved in current directory.")
                
                

def check_sink_demand(model):
    """Check presence of sink and demand reactions.
    
    Here they are simply defined as reactions involving just 1 metabolite, with an ID not starting with "EX_".
    
    Args:
        model (cobra.Model): target model. 
        
    Returns:
        list: IDs of sink/demand reactions found.
    """
    
    found_rids = []
    cnt = 0
    for r in model.reactions:
        if len(r.metabolites) == 1: 
            if r.id.startswith("EX_") == False: 
                cnt += 1
                print(cnt, ':', r.id, ':', r.reaction)
                found_rids.append(r.id)
    
    if found_rids == []:
        print("No sink/demand reactions found.")
    return found_rids
   

                
def check_exr_notation(model): 
    """Check that every EX_change reaction ID begins with "EX_".
    
    Here EX_change reactions are defined as those reactions having just 1 metabolite involved, included in the extracellular compartment.
    
    Args:
        model (cobra.Model): target model. 
        
    Returns:
        list: IDs of EX_change reactions with bad ID.
    """


    found_rids = []
    cnt = 0
    for r in model.reactions:
        if len(r.metabolites) == 1: 
            if list(r.metabolites)[0].id.rsplit('_', 1)[1] == 'e':  # extracellular compartment
                if r.id.startswith("EX_") == False: 
                    cnt += 1
                    print(cnt, ':', r.id, ':', r.reaction)
                    found_rids.append(r.id)
    
    if found_rids == []:
        print("No EX_change reaction with bad ID found.")
    return found_rids

 
    
def remove_EX_annots(model): 
    """Remove all annotations from EX_change reactions.
    
    Args:
        model (cobra.Model): target model. 
    """
    
    cnt = 0
    for r in model.reactions: 
        if len(r.metabolites) == 1 and r.id.startswith("EX_"): 
            if r.annotation != {}: 
                r.annotation = {}

    
    
def check_missing_charges(model):
    """Check if all metabolites have a charge attribute.
    
    Args:
        model (cobra.Model): target model. 
        
    Returns:
        list: IDs of matabolites missing the charge attribute.
    
    """ 
    
    found_mids = []
    cnt = 0
    for m in model.metabolites:  
        cnt += 1
        charge = m.charge
        if charge==None or type(charge)!=int:
            print(cnt, ':', m.id)
            found_mids.append(m.id)
            

    if found_rids == []:
        print("No metabolite with missing charge attribute found.")
    return found_rids



def check_missing_formulas(model):
    """Check if all metabolites have a formula attribute.
    
    Args:
        model (cobra.Model): target model. 
        
    Returns:
        list: IDs of matabolites missing the formula attribute.
    
    """ 
    
    found_mids = []
    cnt = 0
    for m in model.metabolites:  
        formula = m.formula
        if formula==None or formula=='':
            cnt += 1
            print(cnt, ':', m.id)
            found_mids.append(m.id)
            

    if found_mids == []:
        print("No metabolite with missing formula attribute found.")
    return found_mids





def check_artificial_atoms(model):
    """Check if artificial atoms like 'R' and 'X' are present.
    
    Args:
        model (cobra.Model): target model. 
        
    Returns:
        list: IDs of matabolites with artificial atoms.
    """ 
    
    found_mids = []
    cnt = 0
    for m in model.metabolites:  
        formula = m.formula
        if formula == None or formula=='':
            continue  # there are dedicated functions for this
        
        
        # Matches any uppercase letter (A-Z) followed by zero or more lowercase letters (a-z)
        atoms = set(re.findall(r'[A-Z][a-z]*', formula))
        base = set(['C', 'H', 'O', 'N', 'P', 'S'])
        metals = set(['Fe', 'Co', 'As', 'Ca', 'Cd', 'Cl', 'Cu', 'Hg', 'K', 'Mg', 'Mo', 'Na', 'Ni', 'Se', 'Zn', 'Mn'])
        safe_atoms = base.union(metals)
        strange = atoms - safe_atoms
        
        if len(strange) != 0:
            cnt += 1
            print(cnt, ':', m.id, ':', m.formula, ':', atoms) 
            found_mids.append(m.id)

    if found_mids == []:
        print("No metabolite with artificial atoms found.")
    return found_mids



def get_unconstrained_bounds(model): 
    """
    """
    un_lb, un_ub = 0, 0
    for r in model.reactions:
        if r.lower_bound < un_lb: un_lb = r.lower_bound
        if r.upper_bound > un_ub: un_ub = r.upper_bound
    return (un_lb, un_ub)


def reset_unconstrained_bounds(model): 
    """
    """
    un_lb, un_ub = get_unconstrained_bounds(model)
    for r in model.reactions: 
        if r.lower_bound == un_lb: r.lower_bound = -1000
        if r.upper_bound == un_ub: r.upper_bound = 1000



def check_constrained_metabolic(model): 
    """Check the presence of constrained metabolic reactions.
    
    Metabolic reactions are here defined as those having more then 1 involved metabolites.
    Constrained reactions are here defined as those having bounds other then (0, 1000) or (-1000, 1000).
    """
    
    found_rids = []
    cnt = 0
    for r in model.reactions: 
        if len(r.metabolites) == 1: 
            continue # not interested in EXR/sink/demands
            
        if r.bounds != (-1000, 1000) and r.bounds != (0, 1000): 
            cnt += 1
            print(cnt, ':', r.id, ':', r.bounds, ':', r.reaction)
            found_rids.append(r.id)
    
    
    if found_rids == []:
        print("No constrained metabolic reactions found.")
    return found_rids