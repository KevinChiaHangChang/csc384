'''
This file will contain different variable ordering heuristics to be used within
bt_search.

1. ord_dh(csp)
    - Takes in a CSP object (csp).
    - Returns the next Variable to be assigned as per the DH heuristic.
2. ord_mrv(csp)
    - Takes in a CSP object (csp).
    - Returns the next Variable to be assigned as per the MRV heuristic.
3. val_lcv(csp, var)
    - Takes in a CSP object (csp), and a Variable object (var)
    - Returns a list of all of var's potential values, ordered from best value 
      choice to worst value choice according to the LCV heuristic.

The heuristics can use the csp argument (CSP object) to get access to the 
variables and constraints of the problem. The assigned variables and values can 
be accessed via methods.
'''

import random
from copy import deepcopy

def ord_dh(csp):
    # TODO! IMPLEMENT THIS!
    # Degree heuristic
    # Return the variable involved in the largest number of constraints
    # on other unassigned variables
    
    # First get all unassigned variables
    vars = csp.get_all_unasgn_vars()

    # Initialize result
    max_var = vars[0]
    max_deg = 0
    
    # For each variable, sum the links to other unassigned variables across all of its constraints
    for each_var in vars:
        cons = csp.get_cons_with_var(each_var)
        each_deg = 0
        # For each constraint, sum the links to other unassigned variables
        for each_con in cons:
            each_deg += each_con.get_n_unasgn()-1
        if each_deg > max_deg:
            max_deg = each_deg
            max_var = each_var
    return max_var




def ord_mrv(csp):
    # TODO! IMPLEMENT THIS!
    # Minimum Remaining Values heuristic
    # Return the variable with the most constrained current domain
    
    # First get all unassigned variables
    vars = csp.get_all_unasgn_vars()
    # Initialize result
    min_var = vars[0]
    min_dom = vars[0].cur_domain_size()

    # For each variable, count its current domain size
    for each_var in vars:
        each_dom = each_var.cur_domain_size()
        if each_dom < min_dom:
            min_var = each_var
            min_dom = each_dom
    return min_var

def val_lcv(csp, var):
    # TODO! IMPLEMENT THIS!
    # Least Constraining Value heuristic
    # Return list of values for the given variable, 
    # ordered by the value that rules out the fewest 
    # values in remaining variables

    # First get domain of variable
    domain = var.cur_domain()

    # Now get constraints with given variable
    cons = csp.get_cons_with_var(var)

    num_prunes = []
    # For each value of domain, try assigning the value and sum up the number of prunes needed
    for x in domain:
        # Try assigning the value
        var.assign(x)
        num = 0
        # For each constraint, get unassigned variables
        for c in cons:
            # For each unassigned variable, check how much pruning needs to be done
            for each_var in c.get_unasgn_vars():
                for each_val in each_var.cur_domain():
                    if not c.has_support(each_var,each_val):
                        num += 1
        num_prunes.append(num)
        # Remember to unassign the variable
        var.unassign()

    # Sort domain based on num_prunes list
    sorted_values = [x for _,x in sorted(zip(num_prunes,domain))]
    return sorted_values