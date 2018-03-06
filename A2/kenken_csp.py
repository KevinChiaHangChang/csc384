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
    # Initialize var_array
    var_array = []
    for i in range(1,dim+1):
        var_row = []
        for j in range(1,dim+1):
            # Initialize new Variable
            var = Variable("V{}{}".format(i,j),domain)
            # Add variable to var_array
            var_row.append(var)
        var_array.append(var_row)

    # Initialize constraints for CSP
    cons = []
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
                con = Constraint("Binary(V{}{},V{}{})".format(i,j,k,j), [var_a,var_b])

                # Generate satisfying tuples based on domain of the 2 variables
                sat_tuples = []
                for pair in itertools.product(var_a.domain(), var_b.domain()):
                    if pair[0] != pair[1]:
                        sat_tuples.append(pair)
                
                # Add satisfying tuples to constraint
                con.add_satisfying_tuples(sat_tuples)
                cons.append(con)

            # Row constraint
            for k in range(j,dim+1):
                if k <= j:
                    continue
                var_a = var_array[i-1][j-1]
                var_b = var_array[i-1][k-1]
                con = Constraint("Binary(V{}{},V{}{})".format(i,j,i,k), [var_a,var_b])

                # Generate satisfying tuples based on domain of the 2 variables
                sat_tuples = []
                for pair in itertools.product(var_a.domain(), var_b.domain()):
                    if pair[0] != pair[1]:
                        sat_tuples.append(pair)
                
                # Add satisfying tuples to constraint
                con.add_satisfying_tuples(sat_tuples)
                cons.append(con)

    # Initialize CSP
    csp = CSP("Kenken")

    # Add variables
    for var_row in var_array:
        for var in var_row:
            csp.add_var(var)

    # Add constraints
    for con in cons:
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
    # Initialize var_array
    var_array = []
    for i in range(1,dim+1):
        var_row = []
        for j in range(1,dim+1):
            # Initialize new Variable
            var = Variable("V{}{}".format(i,j),domain)
            # Add variable to var_array
            var_row.append(var)
        var_array.append(var_row)

    # Initialize constraints for CSP
    cons = []
    # Now generate n-ary constraints
    # Generate all tuples beforehand
    sat_tuples = []
    for each_tuple in itertools.permutations(domain):
        sat_tuples.append(each_tuple)
    # Row constraint
    for i in range(1,dim+1):
        con = Constraint("All-Diff(Row{})".format(i),var_array[i-1])

        # Generate satisfying tuples based on domain
        # Add satisfying tuples to constraint
        con.add_satisfying_tuples(sat_tuples)
        cons.append(con)

    # Column constraint
    for j in range(1,dim+1):
        col = []
        for i in range(1,dim+1):
            col.append(var_array[i-1][j-1])
        con = Constraint("All-Diff(Column{})".format(j),col)

        # Generate satisfying tuples based on domain
        # Add satisfying tuples to constraint
        con.add_satisfying_tuples(sat_tuples)
        cons.append(con)

    # Initialize CSP
    csp = CSP("Kenken")

    #Add variables
    for var_row in var_array:
        for var in var_row:
            csp.add_var(var)

    # Add constraints
    for con in cons:
        csp.add_constraint(con)

    return csp, var_array


def kenken_csp_model(kenken_grid):
    # TODO! IMPLEMENT THIS!
    # From board dimension N, generate domain for each variable
    dim = kenken_grid[0][0]
    domain = []
    for x in range(1,dim+1):
        domain.append(x)

    # Create NxN board of variables
    # Initialize CSP
    # csp = CSP("Kenken")
    # Initialize var_array
    var_array = []
    for i in range(1,dim+1):
        var_row = []
        for j in range(1,dim+1):
            # Initialize new Variable
            var = Variable("V{}{}".format(i,j),domain)
            # Add variable to var_array
            var_row.append(var)
        var_array.append(var_row)
    
    # Initialize constraints for CSP
    cons = []
    # Now generate cage constraints
    for each_cage in range(1,len(kenken_grid)):
        # Check if cage has two elements or more
        if len(kenken_grid[each_cage]) == 2:
            # Two elements: first element is cell, second element is assigned value
            i_coord = int(str(kenken_grid[each_cage][0])[0])
            j_coord = int(str(kenken_grid[each_cage][0])[1])
            value = kenken_grid[each_cage][1]
            var_array[i_coord-1][j_coord-1] = Variable("V{}{}".format(i_coord,j_coord),[value])
        elif len(kenken_grid[each_cage]) > 2:
            # More than two elements: last element is operator, second last element is target value
            operation = kenken_grid[each_cage][-1]
            target_value = kenken_grid[each_cage][-2]

            # Cage constraint
            # Initialize cage variables array
            cage_vars = []
            # Initialize cage variables domain array, for generating satisfying tuples
            cage_vars_dom = []
            for i in range(0,len(kenken_grid[each_cage])-2):
                # Extract cell coordinates
                i_coord = int(str(kenken_grid[each_cage][i])[0])
                j_coord = int(str(kenken_grid[each_cage][i])[1])
                cell = var_array[i_coord-1][j_coord-1]
                # Add cell to cage variables array
                cage_vars.append(cell)
                # Add cell domain to cage variables domain array
                cage_vars_dom.append(cell.domain())
            con = Constraint("Cage{}".format(each_cage),cage_vars)
            
            # Generate all tuples based on domain 
            # NOTE: tuples may not satisfy cage constraint, must check
            sat_tuples = []
            tuples = []
            if len(cage_vars_dom) > 1:
                tuples = itertools.product(*cage_vars_dom)
            else:
                tuples = cage_vars_dom
            for each_tuple in tuples:
                # Plus operation
                if operation == 0:
                    sum = 0
                    for tmp in each_tuple:
                        sum += tmp
                    if sum == target_value:
                        sat_tuples.append(each_tuple)
                        # print("Append: ",each_tuple)
                # Minus operation
                elif operation == 1:
                    # NOTE: need to try every permutation
                    for each_permutation in itertools.permutations(each_tuple):
                        diff = each_permutation[0]
                        for tmp in range(1,len(each_permutation)):
                            diff -= each_permutation[tmp]
                        if diff == target_value:
                            sat_tuples.append(each_tuple)
                            # print("Append: ",each_tuple)
                # Divide operation
                elif operation == 2:
                    # NOTE: need to try every permutation
                    for each_permutation in itertools.permutations(each_tuple):
                        div = each_permutation[0]
                        for tmp in range(1,len(each_permutation)):
                            div /= each_permutation[tmp]
                        if div == target_value:
                            sat_tuples.append(each_tuple)
                            # print("Append: ",each_tuple)
                # Multiply operation
                elif operation == 3:
                    product = 1
                    for tmp in each_tuple:
                        product *= tmp
                    if product == target_value:
                        sat_tuples.append(each_tuple)
                        # print("Append: ",each_tuple)
                    
            # Add satisfying tuples to constraint
            con.add_satisfying_tuples(sat_tuples)
            cons.append(con)

    # # Now generate n-ary constraints
    # # Generate all tuples beforehand
    # sat_tuples = []
    # for each_tuple in itertools.permutations(domain):
    #     sat_tuples.append(each_tuple)
    # # Row constraint
    # for i in range(1,dim+1):
    #     con = Constraint("All-Diff(Row{})".format(i),var_array[i-1])

    #     # Generate satisfying tuples based on domain
    #     # Add satisfying tuples to constraint
    #     con.add_satisfying_tuples(sat_tuples)
    #     cons.append(con)
    
    # # Column constraint
    # for j in range(1,dim+1):
    #     col = []
    #     for i in range(1,dim+1):
    #         col.append(var_array[i-1][j-1])
    #     con = Constraint("All-Diff(Column{})".format(j),col)

    #     # Generate satisfying tuples based on domain
    #     # Add satisfying tuples to constraint
    #     con.add_satisfying_tuples(sat_tuples)
    #     cons.append(con)

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
                con = Constraint("Binary(V{}{},V{}{})".format(i,j,k,j), [var_a,var_b])

                # Generate satisfying tuples based on domain of the 2 variables
                sat_tuples = []
                for pair in itertools.product(var_a.domain(), var_b.domain()):
                    if pair[0] != pair[1]:
                        sat_tuples.append(pair)
                
                # Add satisfying tuples to constraint
                con.add_satisfying_tuples(sat_tuples)
                cons.append(con)

            # Row constraint
            for k in range(j,dim+1):
                if k <= j:
                    continue
                var_a = var_array[i-1][j-1]
                var_b = var_array[i-1][k-1]
                con = Constraint("Binary(V{}{},V{}{})".format(i,j,i,k), [var_a,var_b])

                # Generate satisfying tuples based on domain of the 2 variables
                sat_tuples = []
                for pair in itertools.product(var_a.domain(), var_b.domain()):
                    if pair[0] != pair[1]:
                        sat_tuples.append(pair)
                
                # Add satisfying tuples to constraint
                con.add_satisfying_tuples(sat_tuples)
                cons.append(con)

    # Initialize CSP
    csp = CSP("Kenken")

    # Add variables
    for var_row in var_array:
        for var in var_row:
            csp.add_var(var)

    # Add constraints
    for con in cons:
        csp.add_constraint(con)

    return csp, var_array
