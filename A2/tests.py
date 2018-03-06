import unittest
import sys
import itertools
import traceback

from cspbase import *
from kenken_csp import *
from propagators import *
from heuristics import *

import propagators

BOARDS = [ [[3],[11,21,3,0],[12,22,2,1],[13,23,33,6,3],[31,32,5,0]],
[[4],[11,21,6,3],[12,13,3,0],[14,24,3,1],[22,23,7,0],[31,32,2,2],[33,43,3,1],[34,44,6,3],[41,42,7,0]],
[[5],[11,21,4,1],[12,13,2,2],[14,24,1,1],[15,25,1,1],[22,23,9,0],[31,32,3,1],[33,34,44,6,3],[35,45,9,0],[41,51,7,0],[42,43,3,1],[52,53,6,3],[54,55,4,1]],
[[6],[11,21,11,0],[12,13,2,2],[14,24,20,3],[15,16,26,36,6,3],[22,23,3,1],[25,35,3,2],[31,32,41,42,240,3],[33,34,6,3],[43,53,6,3],[44,54,55,7,0],[45,46,30,3],[51,52,6,3],[56,66,9,0],[61,62,63,8,0],[64,65,2,2]],
[[5],[11,12,21,22,10,0],[13,14,23,24,34,18,0],[15,25,35,2,1],[31,32,33,1,1],[41,42,43,51,52,53,600,3],[44,54,55,2,2],[45,3]], 
[[6],[11,12,13,2,2],[14,15,3,1],[16,26,36,11,0],[21,22,23,2,2],[24,25,34,35,40,3],[31,41,51,61,14,0],[32,33,42,43,52,53,3600,3],[44,54,64,120,3],[45,46,55,56,1,1],[62,63,5,1],[65,66,5,0]]]

## HELPER FUNCTIONS
def check_diff(vars, board):
    N = board[0][0]
    for i in range(0,N):
        for j in range(0,N):
            #row diff-constraints
            for k in range(j+1,N):
                if vars[i][j].get_assigned_value() == vars[i][k].get_assigned_value():
                    return False
            #col diff-constraints
            for l in range(i+1,N):
                if vars[i][j].get_assigned_value() == vars[l][j].get_assigned_value():
                    return False
    return True
    
def add_check(values, target):
        sum = 0
        for v in values:
            sum += v
        if sum != target:
            return False
        return True

def sub_check(values, target):
        for perm in itertools.permutations(values):
            #calculate value
            result = perm[0]
            i = 1
            while(i < len(values)):
                result -= perm[i]
                i += 1
            if result == target:
                return True
        return False
        
def div_check(values, target):
        for perm in itertools.permutations(values):
            #calculate value
            result = perm[0]
            i = 1
            while(i < len(values)):
                result //= perm[i]
                i += 1
            if result == target:
                return True
        return False
        
def mult_check(values, target):
        prod = 1
        for v in values:
            prod *= v
        if prod != target:
            return False
        return True
    
def check_cages(vars, board):
    N = board[0][0]
    for c in board:
        if len(c) == 1:#board size specification
            continue
        if len(c) == 2:#forced value to a cell
            val = c[1]
            cell_i = (c[0] // 10)-1
            cell_j = (c[0] % 10)-1
            if vars[cell_i][cell_j].get_assigned_value() != val:
                return False
        if len(c) > 2:#larger cage
            val = c[len(c)-2]
            op = c[len(c)-1]
            cage_values = []
            for v in range(0,len(c)-2):#get vars in cage
                cell_i = (c[v] // 10)-1
                cell_j = (c[v] % 10)-1
                cage_values.append(vars[cell_i][cell_j].get_assigned_value())
            if op == 0:
                if add_check(cage_values,val) == False:
                    return False
            elif op == 1:
                if sub_check(cage_values,val) == False:
                    return False
            elif op == 2:
                if div_check(cage_values,val) == False:
                    return False
            elif op ==3:
                if mult_check(cage_values,val) == False:
                    return False
    return True

########################################
##Necessary setup to generate CSP problems

def queensCheck(qi, qj, i, j):
    '''Return true if i and j can be assigned to the queen in row qi and row qj
       respectively. Used to find satisfying tuples.
    '''
    return i != j and abs(i-j) != abs(qi-qj)

def nQueens(n):
    '''Return an n-queens CSP'''
    i = 0
    dom = []
    for i in range(n):
        dom.append(i+1)

    vars = []
    for i in dom:
        vars.append(Variable('Q{}'.format(i), dom))

    cons = []
    for qi in range(len(dom)):
        for qj in range(qi+1, len(dom)):
            con = Constraint("C(Q{},Q{})".format(qi+1,qj+1),[vars[qi], vars[qj]])
            sat_tuples = []
            for t in itertools.product(dom, dom):
                if queensCheck(qi, qj, t[0], t[1]):
                    sat_tuples.append(t)
            con.add_satisfying_tuples(sat_tuples)
            cons.append(con)

    csp = CSP("{}-Queens".format(n), vars)
    for c in cons:
        csp.add_constraint(c)
    return csp

# SPECIFY WHAT TO TEST
TEST_MODELS      = True
TEST_HEURISTICS  = True
TEST_PROPAGATORS = True

class TestStringMethods(unittest.TestCase):
    def helper_prop_none(self, board, prop=prop_FC, var_ord=None, val_lcv=None):
        csp, var_array = kenken_csp_model(board)
        solver = BT(csp)
        solver.quiet()
        solver.bt_search(prop, var_ord, val_lcv)
        self.assertTrue(check_cages(var_array, board), "Incorect value in a cage!")
        self.assertTrue(check_diff(var_array, board), "Repeated value in a row or column!")

    def helper_prop(self, board, prop=prop_FC, var_ord=ord_mrv, val_lcv=None):
        csp, var_array = kenken_csp_model(board)
        solver = BT(csp)
        solver.quiet()
        solver.bt_search(prop, var_ord, val_lcv)
        self.assertTrue(check_cages(var_array, board), "Incorect value in a cage!")
        self.assertTrue(check_diff(var_array, board), "Repeated value in a row or column!")

    def helper_prop_lcv(self, board, prop=prop_FC, var_ord=ord_mrv, val_lcv=val_lcv):
        csp, var_array = kenken_csp_model(board)
        solver = BT(csp)
        solver.quiet()
        solver.bt_search(prop, var_ord, val_lcv)
        self.assertTrue(check_cages(var_array, board), "Incorect value in a cage!")
        self.assertTrue(check_diff(var_array, board), "Repeated value in a row or column!")

    def helper_bne_grid(self, board):
        new_b = []
        for sub_list in board:
            new_b.append(list(sub_list))
        csp, _ = binary_ne_grid(new_b)
        diff_const_count = (board[0][0]+board[0][0])*board[0][0]*(board[0][0]-1)//2 # number of all binary diff constraints
        cons = csp.get_all_cons()
        bin_count = 0 # number of binary constraints
        for c in cons:
            if len(c.get_scope()) == 2:
                bin_count += 1
        self.assertEqual(bin_count, diff_const_count, "Wrong number of binary not equal constraints for binary_ne_grid!")

    # Binary not equal
    @unittest.skipUnless(TEST_MODELS, "Not Testing Models.")
    def test_bne_grid_1(self):
        board = BOARDS[0]
        self.helper_bne_grid(board)

    # Binary not equal
    @unittest.skipUnless(TEST_MODELS, "Not Testing Models.")
    def test_bne_grid_2(self):
        board = BOARDS[1]
        self.helper_bne_grid(board)

    # ADDED TESTS START
    # Binary not equal + FC propagator
    @unittest.skipUnless(TEST_PROPAGATORS and TEST_MODELS, "Not Testing Propagators and Models.")
    def test_props_none_1(self):
        board = BOARDS[0]
        self.helper_prop_none(board)

    # Binary not equal + FC propagator
    @unittest.skipUnless(TEST_PROPAGATORS and TEST_MODELS, "Not Testing Propagators and Models.")
    def test_props_none_2(self):
        board = BOARDS[1]
        self.helper_prop_none(board)

    # Binary not equal + FC propagator
    @unittest.skipUnless(TEST_PROPAGATORS and TEST_MODELS, "Not Testing Propagators and Models.")
    def test_props_none_3(self):
        board = BOARDS[2]
        self.helper_prop_none(board)

    # Binary not equal + GAC propagator
    @unittest.skipUnless(TEST_PROPAGATORS and TEST_MODELS, "Not Testing Propagators and Models.")
    def test_props_none_4(self):
        board = BOARDS[0]
        self.helper_prop_none(board,prop_GAC)

    # Binary not equal + GAC propagator
    @unittest.skipUnless(TEST_PROPAGATORS and TEST_MODELS, "Not Testing Propagators and Models.")
    def test_props_none_5(self):
        board = BOARDS[1]
        self.helper_prop_none(board,prop_GAC)

    # Binary not equal + GAC propagator
    @unittest.skipUnless(TEST_PROPAGATORS and TEST_MODELS, "Not Testing Propagators and Models.")
    def test_props_none_6(self):
        board = BOARDS[2]
        self.helper_prop_none(board,prop_GAC)

    # Binary not equal + FC propagator
    @unittest.skipUnless(TEST_PROPAGATORS and TEST_MODELS, "Not Testing Propagators and Models.")
    def test_props_none_7(self):
        board = BOARDS[3]
        self.helper_prop_none(board)

    # Binary not equal + FC propagator
    @unittest.skipUnless(TEST_PROPAGATORS and TEST_MODELS, "Not Testing Propagators and Models.")
    def test_props_none_8(self):
        board = BOARDS[4]
        self.helper_prop_none(board)

    # Binary not equal + FC propagator
    @unittest.skipUnless(TEST_PROPAGATORS and TEST_MODELS, "Not Testing Propagators and Models.")
    def test_props_none_9(self):
        board = BOARDS[5]
        self.helper_prop_none(board)

    # Binary not equal + GAC propagator
    @unittest.skipUnless(TEST_PROPAGATORS and TEST_MODELS, "Not Testing Propagators and Models.")
    def test_props_none_10(self):
        board = BOARDS[3]
        self.helper_prop_none(board,prop_GAC)

    # Binary not equal + GAC propagator
    @unittest.skipUnless(TEST_PROPAGATORS and TEST_MODELS, "Not Testing Propagators and Models.")
    def test_props_none_11(self):
        board = BOARDS[4]
        self.helper_prop_none(board,prop_GAC)

    # Binary not equal + GAC propagator
    @unittest.skipUnless(TEST_PROPAGATORS and TEST_MODELS, "Not Testing Propagators and Models.")
    def test_props_none_12(self):
        board = BOARDS[5]
        self.helper_prop_none(board,prop_GAC)
    # ADDED TESTS STOP

    # Binary not equal + FC propagator + MRV heuristic
    @unittest.skipUnless(TEST_PROPAGATORS and TEST_MODELS, "Not Testing Propagators and Models.")
    def test_props_1(self):
        board = BOARDS[0]
        self.helper_prop(board)

    # Binary not equal + FC propagator + MRV heuristic
    @unittest.skipUnless(TEST_PROPAGATORS and TEST_MODELS, "Not Testing Propagators and Models.")
    def test_props_2(self):
        board = BOARDS[1]
        self.helper_prop(board)

    # Binary not equal + FC propagator + MRV heuristic
    @unittest.skipUnless(TEST_PROPAGATORS and TEST_MODELS, "Not Testing Propagators and Models.")
    def test_props_3(self):
        board = BOARDS[2]
        self.helper_prop(board)

    # ADDED TESTS START
    # Binary not equal + GAC propagator + MRV heuristic
    @unittest.skipUnless(TEST_PROPAGATORS and TEST_MODELS, "Not Testing Propagators and Models.")
    def test_props_4(self):
        board = BOARDS[0]
        self.helper_prop(board,prop_GAC)

    # Binary not equal + GAC propagator + MRV heuristic
    @unittest.skipUnless(TEST_PROPAGATORS and TEST_MODELS, "Not Testing Propagators and Models.")
    def test_props_5(self):
        board = BOARDS[1]
        self.helper_prop(board,prop_GAC)

    # Binary not equal + GAC propagator + MRV heuristic
    @unittest.skipUnless(TEST_PROPAGATORS and TEST_MODELS, "Not Testing Propagators and Models.")
    def test_props_6(self):
        board = BOARDS[2]
        self.helper_prop(board,prop_GAC)
    # ADDED TESTS STOP

    # ADDED TESTS START
    # Binary not equal + FC propagator + DH heuristic
    @unittest.skipUnless(TEST_PROPAGATORS and TEST_MODELS, "Not Testing Propagators and Models.")
    def test_props_7(self):
        board = BOARDS[0]
        self.helper_prop(board,prop_FC,ord_dh)

    # Binary not equal + FC propagator + DH heuristic
    @unittest.skipUnless(TEST_PROPAGATORS and TEST_MODELS, "Not Testing Propagators and Models.")
    def test_props_8(self):
        board = BOARDS[1]
        self.helper_prop(board,prop_FC,ord_dh)

    # Binary not equal + FC propagator + DH heuristic
    @unittest.skipUnless(TEST_PROPAGATORS and TEST_MODELS, "Not Testing Propagators and Models.")
    def test_props_9(self):
        board = BOARDS[2]
        self.helper_prop(board,prop_FC,ord_dh)
    # # ADDED TESTS STOP

    # ADDED TESTS START
    # Binary not equal + GAC propagator + DH heuristic
    @unittest.skipUnless(TEST_PROPAGATORS and TEST_MODELS, "Not Testing Propagators and Models.")
    def test_props_10(self):
        board = BOARDS[0]
        self.helper_prop(board,prop_GAC,ord_dh)

    # Binary not equal + GAC propagator + DH heuristic
    @unittest.skipUnless(TEST_PROPAGATORS and TEST_MODELS, "Not Testing Propagators and Models.")
    def test_props_11(self):
        board = BOARDS[1]
        self.helper_prop(board,prop_GAC,ord_dh)

    # Binary not equal + GAC propagator + DH heuristic
    @unittest.skipUnless(TEST_PROPAGATORS and TEST_MODELS, "Not Testing Propagators and Models.")
    def test_props_12(self):
        board = BOARDS[2]
        self.helper_prop(board,prop_GAC,ord_dh)
    # ADDED TESTS STOP

    # ADDED TESTS START
    # Binary not equal + FC propagator + MRV heuristic
    @unittest.skipUnless(TEST_PROPAGATORS and TEST_MODELS, "Not Testing Propagators and Models.")
    def test_props_13(self):
        board = BOARDS[3]
        self.helper_prop(board)

    # Binary not equal + FC propagator + MRV heuristic
    @unittest.skipUnless(TEST_PROPAGATORS and TEST_MODELS, "Not Testing Propagators and Models.")   
    def test_props_14(self):
        board = BOARDS[4]
        self.helper_prop(board)

    # Binary not equal + FC propagator + MRV heuristic
    @unittest.skipUnless(TEST_PROPAGATORS and TEST_MODELS, "Not Testing Propagators and Models.")
    def test_props_15(self):
        board = BOARDS[5]
        self.helper_prop(board)
    # ADDED TESTS STOP

    # Binary not equal + GAC propagator + MRV heuristic
    @unittest.skipUnless(TEST_PROPAGATORS and TEST_MODELS, "Not Testing Propagators and Models.")
    def test_props_16(self):
        board = BOARDS[3]
        self.helper_prop(board, prop_GAC)

    # Binary not equal + GAC propagator + MRV heuristic
    @unittest.skipUnless(TEST_PROPAGATORS and TEST_MODELS, "Not Testing Propagators and Models.")   
    def test_props_17(self):
        board = BOARDS[4]
        self.helper_prop(board, prop_GAC)

    # Binary not equal + GAC propagator + MRV heuristic
    @unittest.skipUnless(TEST_PROPAGATORS and TEST_MODELS, "Not Testing Propagators and Models.")
    def test_props_18(self):
        board = BOARDS[5]
        self.helper_prop(board, prop_GAC)

    # ADDED TESTS START
    # Binary not equal + FC propagator + DH heuristic
    # @unittest.skipUnless(TEST_PROPAGATORS and TEST_MODELS, "Not Testing Propagators and Models.")
    # def test_props_19(self):
    #     board = BOARDS[3]
    #     self.helper_prop(board, prop_FC, ord_dh)

    # # Binary not equal + FC propagator + DH heuristic
    # @unittest.skipUnless(TEST_PROPAGATORS and TEST_MODELS, "Not Testing Propagators and Models.")   
    # def test_props_20(self):
    #     board = BOARDS[4]
    #     self.helper_prop(board, prop_FC, ord_dh)

    # # Binary not equal + FC propagator + DH heuristic
    # @unittest.skipUnless(TEST_PROPAGATORS and TEST_MODELS, "Not Testing Propagators and Models.")
    # def test_props_21(self):
    #     board = BOARDS[5]
    #     self.helper_prop(board, prop_FC, ord_dh)
    # ADDED TESTS STOP

    # ADDED TESTS START
    # Binary not equal + GAC propagator + DH heuristic
    @unittest.skipUnless(TEST_PROPAGATORS and TEST_MODELS, "Not Testing Propagators and Models.")
    def test_props_22(self):
        board = BOARDS[3]
        self.helper_prop(board, prop_GAC, ord_dh)

    # Binary not equal + GAC propagator + DH heuristic
    @unittest.skipUnless(TEST_PROPAGATORS and TEST_MODELS, "Not Testing Propagators and Models.")   
    def test_props_23(self):
        board = BOARDS[4]
        self.helper_prop(board, prop_GAC, ord_dh)

    # Binary not equal + GAC propagator + DH heuristic
    @unittest.skipUnless(TEST_PROPAGATORS and TEST_MODELS, "Not Testing Propagators and Models.")
    def test_props_24(self):
        board = BOARDS[5]
        self.helper_prop(board, prop_GAC, ord_dh)
    # ADDED TESTS STOP

    # ADDED TESTS START
    # Binary not equal + FC propagator + MRV heuristic + LCV heuristic
    @unittest.skipUnless(TEST_PROPAGATORS and TEST_MODELS, "Not Testing Propagators and Models.")
    def test_props_lcv_1(self):
        board = BOARDS[0]
        self.helper_prop_lcv(board)

    # Binary not equal + FC propagator + MRV heuristic + LCV heuristic
    @unittest.skipUnless(TEST_PROPAGATORS and TEST_MODELS, "Not Testing Propagators and Models.")
    def test_props_lcv_2(self):
        board = BOARDS[1]
        self.helper_prop_lcv(board)

    # Binary not equal + FC propagator + MRV heuristic + LCV heuristic
    @unittest.skipUnless(TEST_PROPAGATORS and TEST_MODELS, "Not Testing Propagators and Models.")
    def test_props_lcv_3(self):
        board = BOARDS[2]
        self.helper_prop_lcv(board)

    # Binary not equal + GAC propagator + MRV heuristic + LCV heuristic
    @unittest.skipUnless(TEST_PROPAGATORS and TEST_MODELS, "Not Testing Propagators and Models.")
    def test_props_lcv_4(self):
        board = BOARDS[0]
        self.helper_prop_lcv(board,prop_GAC)

    # Binary not equal + GAC propagator + MRV heuristic + LCV heuristic
    @unittest.skipUnless(TEST_PROPAGATORS and TEST_MODELS, "Not Testing Propagators and Models.")
    def test_props_lcv_5(self):
        board = BOARDS[1]
        self.helper_prop_lcv(board,prop_GAC)

    # Binary not equal + GAC propagator + MRV heuristic + LCV heuristic
    @unittest.skipUnless(TEST_PROPAGATORS and TEST_MODELS, "Not Testing Propagators and Models.")
    def test_props_lcv_6(self):
        board = BOARDS[2]
        self.helper_prop_lcv(board,prop_GAC)
    
    # Binary not equal + FC propagator + DH heuristic + LCV heuristic
    @unittest.skipUnless(TEST_PROPAGATORS and TEST_MODELS, "Not Testing Propagators and Models.")
    def test_props_lcv_7(self):
        board = BOARDS[0]
        self.helper_prop(board,prop_FC,ord_dh)

    # Binary not equal + FC propagator + DH heuristic + LCV heuristic
    @unittest.skipUnless(TEST_PROPAGATORS and TEST_MODELS, "Not Testing Propagators and Models.")
    def test_props_lcv_8(self):
        board = BOARDS[1]
        self.helper_prop(board,prop_FC,ord_dh)

    # Binary not equal + FC propagator + DH heuristic + LCV heuristic
    @unittest.skipUnless(TEST_PROPAGATORS and TEST_MODELS, "Not Testing Propagators and Models.")
    def test_props_lcv_9(self):
        board = BOARDS[2]
        self.helper_prop(board,prop_FC,ord_dh)

    # Binary not equal + GAC propagator + DH heuristic + LCV heuristic
    @unittest.skipUnless(TEST_PROPAGATORS and TEST_MODELS, "Not Testing Propagators and Models.")
    def test_props_lcv_10(self):
        board = BOARDS[0]
        self.helper_prop(board,prop_GAC,ord_dh)

    # Binary not equal + GAC propagator + DH heuristic + LCV heuristic
    @unittest.skipUnless(TEST_PROPAGATORS and TEST_MODELS, "Not Testing Propagators and Models.")
    def test_props_lcv_11(self):
        board = BOARDS[1]
        self.helper_prop(board,prop_GAC,ord_dh)

    # Binary not equal + GAC propagator + DH heuristic + LCV heuristic
    @unittest.skipUnless(TEST_PROPAGATORS and TEST_MODELS, "Not Testing Propagators and Models.")
    def test_props_lcv_12(self):
        board = BOARDS[2]
        self.helper_prop(board,prop_GAC,ord_dh)

    # Binary not equal + FC propagator + MRV heuristic + LCV heuristic
    @unittest.skipUnless(TEST_PROPAGATORS and TEST_MODELS, "Not Testing Propagators and Models.")
    def test_props_lcv_13(self):
        board = BOARDS[3]
        self.helper_prop_lcv(board)

    # Binary not equal + FC propagator + MRV heuristic + LCV heuristic
    @unittest.skipUnless(TEST_PROPAGATORS and TEST_MODELS, "Not Testing Propagators and Models.")
    def test_props_lcv_14(self):
        board = BOARDS[4]
        self.helper_prop_lcv(board)

    # Binary not equal + FC propagator + MRV heuristic + LCV heuristic
    @unittest.skipUnless(TEST_PROPAGATORS and TEST_MODELS, "Not Testing Propagators and Models.")
    def test_props_lcv_15(self):
        board = BOARDS[5]
        self.helper_prop_lcv(board)

    # Binary not equal + GAC propagator + MRV heuristic + LCV heuristic
    @unittest.skipUnless(TEST_PROPAGATORS and TEST_MODELS, "Not Testing Propagators and Models.")
    def test_props_lcv_16(self):
        board = BOARDS[3]
        self.helper_prop_lcv(board,prop_GAC)

    # Binary not equal + GAC propagator + MRV heuristic + LCV heuristic
    @unittest.skipUnless(TEST_PROPAGATORS and TEST_MODELS, "Not Testing Propagators and Models.")
    def test_props_lcv_17(self):
        board = BOARDS[4]
        self.helper_prop_lcv(board,prop_GAC)

    # Binary not equal + GAC propagator + MRV heuristic + LCV heuristic
    @unittest.skipUnless(TEST_PROPAGATORS and TEST_MODELS, "Not Testing Propagators and Models.")
    def test_props_lcv_18(self):
        board = BOARDS[5]
        self.helper_prop_lcv(board,prop_GAC)
    
    # ADDED TESTS STOP

    @unittest.skipUnless(TEST_HEURISTICS, "Not Testing Heuristics.")
    def test_ord_mrv_1(self):
        a = Variable('A', [1])
        b = Variable('B', [1])
        c = Variable('C', [1])
        d = Variable('D', [1])
        e = Variable('E', [1])
        simpleCSP = CSP("Simple", [a,b,c,d,e])
        count = 0
        for i in range(0,len(simpleCSP.vars)):
            simpleCSP.vars[count].add_domain_values(range(0, count))
            count += 1
        var = []
        var = ord_mrv(simpleCSP)
        self.assertEqual(var.name, simpleCSP.vars[0].name, "MRV Picked the wrong variable")

    @unittest.skipUnless(TEST_HEURISTICS, "Not Testing Heuristics.")
    def test_ord_mrv_2(self):
        a = Variable('A', [1,2,3,4,5])
        b = Variable('B', [1,2,3,4])
        c = Variable('C', [1,2])
        d = Variable('D', [1,2,3])
        e = Variable('E', [1])
        simpleCSP = CSP("Simple", [a,b,c,d,e])
        var = []
        var = ord_mrv(simpleCSP)
        self.assertEqual(var.name, simpleCSP.vars[len(simpleCSP.vars)-1].name, "MRV Picked the wrong variable")
    
    # ADD TESTS START
    @unittest.skipUnless(TEST_HEURISTICS, "Not Testing Heuristics.")
    def test_ord_dh_1(self):
        # Use in class example
        domain1 = list(range(10))
        domain2 = list(range(2))
        # Define variables
        f = Variable('f',domain2)
        t = Variable('t',domain1)
        u = Variable('u',domain1)
        r = Variable('r',domain1)
        w = Variable('w',domain1)
        o = Variable('o',domain1)
        c3 = Variable('c3',domain2)
        c1 = Variable('c1',domain2)
        c2 = Variable('c2',domain2)
        # Add variables
        csp = CSP("Example",[f,t,u,r,w,o,c3,c1,c2])
        # Add constraints
        # All-Diff Constraint
        all_diff = Constraint("All-Diff",[t,w,o,f,u,r])
        sat_tuples = []
        for each_tuple in itertools.permutations(domain1,r=6):
            sat_tuples.append(each_tuple)
        all_diff.add_satisfying_tuples(sat_tuples)
        csp.add_constraint(all_diff)
        # Add numerical constraints
        num1 = Constraint("Num1",[o,r,c1])
        sat_tuples = []
        domains = [domain1,domain1,domain2]
        for each_tuple in itertools.product(*domains):
            if 2*each_tuple[0] == each_tuple[1] + 10*each_tuple[2]:
                sat_tuples.append(each_tuple)
        num1.add_satisfying_tuples(sat_tuples)
        csp.add_constraint(num1)
        num2 = Constraint("Num2",[w,c1,u,c2])
        sat_tuples = []
        domains = [domain1,domain2,domain1,domain2]
        for each_tuple in itertools.product(*domains):
            if 2*each_tuple[0] + each_tuple[1] == each_tuple[2] + 10*each_tuple[3]:
                sat_tuples.append(each_tuple)
        num2.add_satisfying_tuples(sat_tuples)
        csp.add_constraint(num2)
        num3 = Constraint("Num3",[t,c2,o,c3])
        sat_tuples = []
        domains = [domain1,domain2,domain1,domain2]
        for each_tuple in itertools.product(*domains):
            if 2*each_tuple[0] + each_tuple[1] == each_tuple[2] + 10*each_tuple[3]:
                sat_tuples.append(each_tuple)
        num3.add_satisfying_tuples(sat_tuples)
        csp.add_constraint(num3)
        num4 = Constraint("Num4",[f,c3])
        sat_tuples = []
        for each_tuple in itertools.permutations(domain2, r=2):
            sat_tuples.append(each_tuple)
        num4.add_satisfying_tuples(sat_tuples)
        csp.add_constraint(num4)
        var = []
        var = ord_dh(csp)
        self.assertEqual(var.name, o.name, "DH Picked the wrong variable")
    # ADD TESTS STOP

    # ADD TESTS START
    @unittest.skipUnless(TEST_HEURISTICS, "Not Testing Hueristics.")
    def test_val_lcv_1(self):
        # TODO
        self.assertTrue(True)
    # ADD TESTS STOP

    ##Tests FC after the first queen is placed in position 1.
    @unittest.skipUnless(TEST_PROPAGATORS, "Not Testing Propagotors.")
    def test_simple_FC(self):
        queens = nQueens(8)
        curr_vars = queens.get_all_vars()
        curr_vars[0].assign(1)
        propagators.prop_FC(queens,newVar=curr_vars[0])
        answer = [[1],[3, 4, 5, 6, 7, 8],[2, 4, 5, 6, 7, 8],[2, 3, 5, 6, 7, 8],[2, 3, 4, 6, 7, 8],[2, 3, 4, 5, 7, 8],[2, 3, 4, 5, 6, 8],[2, 3, 4, 5, 6, 7]]
        var_domain = [x.cur_domain() for x in curr_vars]
        for i in range(len(curr_vars)):
            self.assertEqual(var_domain[i], answer[i], "Failed simple FC test: variable domains don't match expected results")

    # ADD TESTS START
    ## Tests GAC after the first queen is placed in position 2
    def test_simple_GAC(self):
        queens = nQueens(8)
        curr_vars = queens.get_all_vars()
        curr_vars[0].assign(1)
        propagators.prop_GAC(queens,newVar=curr_vars[0])
        answer = [[1],[3,4,5,6,7,8],[2,4,5,6,7,8],[2,3,5,6,7,8],[2,3,4,6,7,8],[2,3,4,5,7,8],[2,3,4,5,6,8],[2,3,4,5,6,7]]
        var_domain = [x.cur_domain() for x in curr_vars]
        for i in range(len(curr_vars)):
            self.assertEqual(var_domain[i], answer[i], "Failed simple GAC test: variable domains don't match expected results")
    # ADD TESTS STOP

    @unittest.skipUnless(TEST_PROPAGATORS, "Not Testing Propagotors.")
    def test_DWO_FC(self):
        queens = nQueens(6)
        cur_var = queens.get_all_vars()
        cur_var[0].assign(2)
        pruned = propagators.prop_FC(queens,newVar=cur_var[0])
        self.assertTrue(pruned[0], "Failed a FC test: returned DWO too early.")
        cur_var[1].assign(5)
        pruned = propagators.prop_FC(queens,newVar=cur_var[1])
        self.assertTrue(pruned[0], "Failed a FC test: returned DWO too early.")
        cur_var[4].assign(1)
        pruned = propagators.prop_FC(queens,newVar=cur_var[4])

        self.assertFalse(pruned[0], "Failed a FC test: should have resulted in a DWO")

    # ADD TESTS START
    @unittest.skipUnless(TEST_PROPAGATORS, "Not Testing Propagotors.")
    def test_DWO_GAC(self):
        queens = nQueens(6)
        cur_var = queens.get_all_vars()
        cur_var[0].assign(2)
        pruned = propagators.prop_GAC(queens,newVar=cur_var[0])
        self.assertTrue(pruned[0], "Failed a FC test: should have resulted in a DWO")
        cur_var[1].assign(5)
        pruned = propagators.prop_GAC(queens,newVar=cur_var[1])

        self.assertFalse(pruned[0], "Failed a FC test: should a resulted in a DWO")
    # ADD TESTS STOP

if __name__ == '__main__':
    unittest.main()