#Look for #IMPLEMENT tags in this file.
'''
All models need to return a CSP object, and a list of lists of Variable objects 
representing the board. The returned list of lists is used to access the 
solution. 

For example, after these three lines of code

    csp, var_array = futoshiki_csp_model_1(board)
    solver = BT(csp)
    solver.bt_search(prop_FC, var_ord)

var_array[0][0].get_assigned_value() should be the correct value in the top left
cell of the Futoshiki puzzle.

1. futoshiki_csp_model_1 (worth 20/100 marks)
    - A model of a Futoshiki grid built using only 
      binary not-equal constraints for both the row and column constraints.

2. futoshiki_csp_model_2 (worth 20/100 marks)
    - A model of a Futoshiki grid built using only n-ary 
      all-different constraints for both the row and column constraints. 

'''
from cspbase import *
import itertools

def futoshiki_csp_model_1(futo_grid):
    # Definition of CSP obj:
    # def __init__(self, name, vars=[]):
    #     '''create a CSP object. Specify a name (a string) and 
    #        optionally a set of variables'''

    #     self.name = name
    #     self.vars = []
    #     self.cons = []
    #     self.vars_to_cons = dict()
    #     for v in vars:
    #         self.add_var(v)

    # Definition of Variable obj:
    # def __init__(self, name, domain=[]):
    #     '''Create a variable object, specifying its name (a
    #     string). Optionally specify the initial domain.
    #     '''
    #     self.name = name                #text name for variable
    #     self.dom = list(domain)         #Make a copy of passed domain
    #     self.curdom = [True] * len(domain)      #using list
    #     #for bt_search
    #     self.assignedValue = None
    n = len(futo_grid) # dimension of the board
    csp = CSP("model2")
    var_array = []
    cond_array = {}
    #Initiailize all Variables since we know their location at all times
    for row_index, row in enumerate(futo_grid): # we will initialize row-by-row
        vars_row = []
        for col_index, item in enumerate(row): # going through items in the list thatg breaks down every row
            if col_index % 2 == 0 and item == 0: # no value in futo_grid = full domain of values
                domain = list(range(1, n + 1))
                successful_var = Variable("V[{0}][{1}]".format(row_index, (col_index // 2)), domain)
                vars_row.append(successful_var)
                csp.add_var(successful_var)
            elif (col_index % 2 == 0 and item != 0): # value provided = this is the domain for this cell 
                domain = [item]
                successful_var = Variable("V[{0}][{1}]".format(row_index, (col_index // 2)), domain)
                successful_var.assign(item)
                vars_row.append(successful_var)
                csp.add_var(successful_var)
            elif col_index % 2 == 1 and item in [">","<"]:
                cond_array[((row_index, (col_index // 2)), (row_index, ((col_index+2) // 2)))] = item
                
        var_array.append(vars_row)
        # cond_array.append(condition_row)
    
    length_var_array = len(var_array)
    for index_row in range(len(var_array)):
        for index_col1, index_col2 in itertools.combinations(range(len(var_array)),2):
                        # range(len(var_array)-1):
                row_var1 = var_array[index_row][index_col1]
                row_var2 = var_array[index_row][index_col2]
                C = Constraint("C[{0}][{1}][{2}][{3}]".format(index_row, index_col1, index_row, index_col2), [row_var1, row_var2])
                list_of_values = itertools.product(row_var1.cur_domain(),row_var2.cur_domain())
                sat_tuples = []
                for tup in list_of_values:
                    if tup[0] != tup[1]:
                        if cond_array.get(((index_row, index_col1),(index_row, index_col2)),"") == ">":
                            if tup[0]>tup[1]:
                                sat_tuples.append(tup)
                        elif (cond_array.get(((index_row, index_col1),(index_row, index_col2)),"") == "<"):
                            if tup[0]<tup[1]:
                                sat_tuples.append(tup)
                        else:
                            sat_tuples.append(tup)
                C.add_satisfying_tuples(sat_tuples)
                csp.add_constraint(C)
            #do the same for vertical
                col_var1 = var_array[index_col1][index_row]
                col_var2 = var_array[index_col2][index_row]
                C = Constraint("C[{0}][{1}][{2}][{3}]".format(index_col1, index_row, index_col2, index_row), [col_var1, col_var2])
                list_of_values = itertools.product(col_var1.cur_domain(),col_var2.cur_domain())
                sat_tuples = []
                for tup in list_of_values:
                    if tup[0] != tup[1]:
                        sat_tuples.append(tup)
                C.add_satisfying_tuples(sat_tuples)
                csp.add_constraint(C)
    return csp, var_array
    

def futoshiki_csp_model_2(futo_grid):
    n = len(futo_grid) # dimension of the board
    csp = CSP("model1")
    var_array = []
    cond_array = {}
    #Initiailize all Variables since we know their location at all times
    for row_index, row in enumerate(futo_grid): # we will initialize row-by-row
        vars_row = []
        for col_index, item in enumerate(row): # going through items in the list thatg breaks down every row
            if col_index % 2 == 0 and item == 0: # no value in futo_grid = full domain of values
                domain = list(range(1, n + 1))
                successful_var = Variable("V[{0}][{1}]".format(row_index, (col_index // 2)), domain)
                vars_row.append(successful_var)
                csp.add_var(successful_var)
            elif (col_index % 2 == 0 and item != 0): # value provided = this is the domain for this cell 
                domain = [item]
                successful_var = Variable("V[{0}][{1}]".format(row_index, (col_index // 2)), domain)
                successful_var.assign(item)
                vars_row.append(successful_var)
                csp.add_var(successful_var)
            elif col_index % 2 == 1 and item in [">","<"]:
                cond_array[((row_index, (col_index // 2)), (row_index, ((col_index+2) // 2)))] = item
                
        var_array.append(vars_row)
        # cond_array.append(condition_row)
    
    length_var_array = len(var_array)
    for index_row in range(len(var_array)):
        for index_col1, index_col2 in itertools.combinations(range(len(var_array)),2):
                        # range(len(var_array)-1):
                row_var1 = var_array[index_row][index_col1]
                row_var2 = var_array[index_row][index_col2]
                C = Constraint("C[{0}][{1}][{2}][{3}]".format(index_row, index_col1, index_row, index_col2), [row_var1, row_var2])
                list_of_values = itertools.product(row_var1.cur_domain(),row_var2.cur_domain())
                sat_tuples = []
                for tup in list_of_values:
                    if tup[0] != tup[1]:
                        if cond_array.get(((index_row, index_col1),(index_row, index_col2)),"") == ">":
                            if tup[0]>tup[1]:
                                sat_tuples.append(tup)
                        elif (cond_array.get(((index_row, index_col1),(index_row, index_col2)),"") == "<"):
                            if tup[0]<tup[1]:
                                sat_tuples.append(tup)
                C.add_satisfying_tuples(sat_tuples)
                csp.add_constraint(C)
            #do the same for vertical
                col_var1 = var_array[index_col1][index_row]
                col_var2 = var_array[index_col2][index_row]
                C = Constraint("C[{0}][{1}][{2}][{3}]".format(index_col1, index_row, index_col2, index_row), [col_var1, col_var2])
                list_of_values = itertools.product(col_var1.cur_domain(),col_var2.cur_domain())
                sat_tuples = []
                for tup in list_of_values:
                    if tup[0] != tup[1]:
                        sat_tuples.append(tup)
                C.add_satisfying_tuples(sat_tuples)
                csp.add_constraint(C)
    return csp, var_array
   
