from cspbase import *
import itertools

'''
All models need to return a CSP object, and a list of lists of Variable objects 
representing the board. The returned list of lists is used to access the 
solution. 

For example, after these three lines of code

    csp, var_array = kenken_csp_model(board)
    solver = BT(csp)
    solver.bt_search(prop_FC, var_ord)

var_array[0][0].get_assigned_value() should be the correct value in the top left
cell of the KenKen puzzle.

The grid-only models do not need to encode the cage constraints.

1. binary_ne_grid (worth 10/100 marks)
    - A model of a KenKen grid (without cage constraints) built using only 
      binary not-equal constraints for both the row and column constraints.

2. nary_ad_grid (worth 10/100 marks)
    - A model of a KenKen grid (without cage constraints) built using only n-ary 
      all-different constraints for both the row and column constraints. 

3. kenken_csp_model (worth 20/100 marks) 
    - A model built using your choice of (1) binary binary not-equal, or (2) 
      n-ary all-different constraints for the grid.
    - Together with KenKen cage constraints.

'''

def binary_ne_grid(kenken_grid):
    # TODO! IMPLEMENT THIS!
    # From board dimension N, generate domain for each variable
    dim = kenken_grid[0][0]
    domain = []
    for x in range(1,dim+1):
        domain.append(x)
    
    # Don't care about cage, just create NxN board of variables
    # Initialize CSP
    csp = CSP("Kenken",[])
    # Initialize var_array
    var_array = []
    for i in domain:
        var_row = []
        for j in domain:
            # Initialize new Variable
            var = Variable("Var[{}][{}]".format(i,j),domain)
            # Add variable to var_array
            var_row.append(var)
            # Add variable to CSP
            csp.add_var(var)
        var_array.append(var_row)

    # Now generate binary not-equal constraints
    for i in range(1,dim+1):
        for j in range(1,dim+1):
            # Column constraint
            for k in range(i,dim+1):
                # Make sure not to add the same constraint twice
                if k <= i:
                    continue
                # Initialize new column constraint
                var_a = var_array[i-1][j-1]
                var_b = var_array[k-1][j-1]
                con = Constraint("C(Var[{}][{}],Var[{}][{}])".format(i,j,k,j), [var_a,var_b])

                # Generate satisfying tuples based on domain of the 2 variables
                sat_tuples = []
                for pair in itertools.product(var_a.domain(), var_b.domain()):
                    if pair[0] != pair[1]:
                        sat_tuples.append(pair)
                
                # Add satisfying tuples to constraint
                con.add_satisfying_tuples(sat_tuples)
                # Add constraint to CSP
                csp.add_constraint(con)

            # Row constraint
            for k in range(j,dim+1):
                if k <= j:
                    continue
                var_a = var_array[i-1][j-1]
                var_b = var_array[i-1][k-1]
                con = Constraint("C(Var[{}][{}],Var[{}][{}])".format(i,j,i,k), [var_a,var_b])

                # Generate satisfying tuples based on domain of the 2 variables
                sat_tuples = []
                for pair in itertools.product(var_a.domain(), var_b.domain()):
                    if pair[0] != pair[1]:
                        sat_tuples.append(pair)
                
                # Add satisfying tuples to constraint
                con.add_satisfying_tuples(sat_tuples)
                # Add constraint to CSP
                csp.add_constraint(con)

    return csp, var_array

def nary_ad_grid(kenken_grid):
    # TODO! IMPLEMENT THIS!
    # From board dimension N, generate domain for each variable
    dim = kenken_grid[0][0]
    domain = []
    for x in range(1,dim+1):
        domain.append(x)

    # Don't care about cage, just create NxN board of variables
    # Initialize CSP
    csp = CSP("Kenken",[])
    # Initialize var_array
    var_array = []
    for i in domain:
        var_row = []
        for j in domain:
            # Initialize new Variable
            var = Variable("Var[{}][{}]".format(i,j),domain)
            # Add variable to var_array
            var_row.append(var)
            # Add variable to CSP
            csp.add_var(var)
        var_array.append(var_row)

    # Now generate n-ary constraints
    # Generate all permutations beforehand
    permutations = itertools.permutations(domain)
    # Row constraint
    for i in range(1,dim+1):
        con = Constraint("All-Diff(Row[{}])".format(i),var_array[i-1])

        # Generate satisfying tuples based on domain
        # Add satisfying tuples to constraint
        con.add_satisfying_tuples(permutations)
        # Add constraint to CSP
        csp.add_constraint(con)
    
    # Column constraint
    for j in range(1,dim+1):
        vars = []
        for i in range(1,dim+1):
            vars.append(var_array[i-1][j-1])
        con = Constraint("All-Diff(Column[{}]".format(j),vars)

        # Generate satisfying tuples based on domain
        # Add satisfying tuples to constraint
        con.add_satisfying_tuples(perutations)
        # Add constraint to CSP
        csp.add_constraint(con)
    
    return csp, var_array


def kenken_csp_model(kenken_grid):
    # TODO! IMPLEMENT THIS!
    