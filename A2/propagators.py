'''
This file will contain different constraint propagators to be used within 
bt_search.

---
A propagator is a function with the following header
    propagator(csp, newly_instantiated_variable=None)

csp is a CSP object---the propagator can use this to get access to the variables 
and constraints of the problem. The assigned variables can be accessed via 
methods, the values assigned can also be accessed.

newly_instantiated_variable is an optional argument. SEE ``PROCESSING REQUIRED''
if newly_instantiated_variable is not None:
    then newly_instantiated_variable is the most
    recently assigned variable of the search.
else:
    propagator is called before any assignments are made
    in which case it must decide what processing to do
    prior to any variables being assigned. 

The propagator returns True/False and a list of (Variable, Value) pairs, like so
    (True/False, [(Variable, Value), (Variable, Value) ...]

Propagators will return False if they detect a dead-end. In this case, bt_search 
will backtrack. Propagators will return true if we can continue.

The list of variable value pairs are all of the values that the propagator 
pruned (using the variable's prune_value method). bt_search NEEDS to know this 
in order to correctly restore these values when it undoes a variable assignment.

Propagators SHOULD NOT prune a value that has already been pruned! Nor should 
they prune a value twice.

---

PROCESSING REQUIRED:
When a propagator is called with newly_instantiated_variable = None:

1. For plain backtracking (where we only check fully instantiated constraints)
we do nothing...return true, []

2. For FC (where we only check constraints with one remaining 
variable) we look for unary constraints of the csp (constraints whose scope 
contains only one variable) and we forward_check these constraints.

3. For GAC we initialize the GAC queue with all constaints of the csp.

When a propagator is called with newly_instantiated_variable = a variable V

1. For plain backtracking we check all constraints with V (see csp method
get_cons_with_var) that are fully assigned.

2. For forward checking we forward check all constraints with V that have one 
unassigned variable left

3. For GAC we initialize the GAC queue with all constraints containing V.

'''

def prop_BT(csp, newVar=None):
    '''
    Do plain backtracking propagation. That is, do no propagation at all. Just 
    check fully instantiated constraints.
    '''
    if not newVar:
        return True, []
    for c in csp.get_cons_with_var(newVar):
        if c.get_n_unasgn() == 0:
            vals = []
            vars = c.get_scope()
            for var in vars:
                vals.append(var.get_assigned_value())
            if not c.check(vals):
                return False, []
    return True, []

def prop_FC(csp, newVar=None):
    # TODO! IMPLEMENT THIS!
    prune_list = []
    if not newVar:
        # Forward check all unuary constraints
        for c in csp.get_all_cons():
            # Check that the constraint has only 1 unassigned variable
            if c.get_n_unasgn() == 1:
                vals = []
                vars = c.get_scope()
                unasgn_var = c.get_unasgn_vars()[0]
                # Copy all assigned variable values, unassigned variable will return value None
                for each_var in vars:
                    vals.append(each_var.get_assigned_value())
                # Find index of unassigned variable
                unasgn_var_idx = vars.index(unasgn_var)
                # Get domain of unassigned variable
                domain = unasgn_var.cur_domain()
                for x in domain:
                    # Try each value in domain
                    vals[unasgn_var_idx] = x
                    if not c.check(vals):
                        # Prune value from variable domain
                        unasgn_var.prune_value(x)
                        # Push into prune list
                        prune_list.append((unasgn_var,x))
                # Check if Domain Wipe Out
                if unasgn_var.cur_domain_size() == 0:
                    return False, prune_list
        return True, prune_list
    else:
        # Forward check all unary constraints with newVar
        for c in csp.get_cons_with_var(newVar):
            # Check that the constraint has only 1 unassigned variable
            if c.get_n_unasgn() == 1:
                vals = []
                vars = c.get_scope()
                unasgn_var = c.get_unasgn_vars()[0]
                # Copy all assigned variable values, unassigned variable will return value None
                for each_var in vars:
                    vals.append(each_var.get_assigned_value())
                # Find index of unassigned variable
                unasgn_var_idx = vars.index(unasgn_var)
                # Get domain of unassigned variable
                domain = unasgn_var.cur_domain()
                for x in domain:
                    # Try each value in domain
                    vals[unasgn_var_idx] = x
                    if not c.check(vals):
                        # Prune value from variable domain
                        unasgn_var.prune_value(x)
                        # Push into prune list
                        prune_list.append((unasgn_var,x))
                # Check if Domain Wipe Out
                if unasgn_var.cur_domain_size() == 0:
                    return False, prune_list
        return True, prune_list

def prop_GAC(csp, newVar=None):
    '''
    Do GAC propagation. If newVar is None we do initial GAC enforce processing 
    all constraints. Otherwise we do GAC enforce with constraints containing 
    newVar on GAC Queue.
    '''
    # TODO! IMPLEMENT THIS!
    
