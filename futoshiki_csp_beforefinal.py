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
    
    for index_row in range(len(var_array)):
        for index_col1, index_col2 in itertools.combinations(range(len(var_array)),2): # go over all rows and cols
                row_var1 = var_array[index_row][index_col1]
                row_var2 = var_array[index_row][index_col2]
                C = Constraint("C[{0}][{1}][{2}][{3}]".format(index_row, index_col1, index_row, index_col2), [row_var1, row_var2]) # build a constraint with the given set of 2 vars
                list_of_values = itertools.product(row_var1.cur_domain(),row_var2.cur_domain()) # produce all possible combinations between 2 domains
                sat_tuples = [] # satisfying tuples to add to constraint
                for tup in list_of_values: # Checking conditions in between each value of the tuple (if there is a condition to begin with)
                    if tup[0] != tup[1]:
                        if cond_array.get(((index_row, index_col1),(index_row, index_col2)),"") == ">":
                            if tup[0]>tup[1]:
                                if tup not in sat_tuples:
                                        sat_tuples.append(tup)
                        elif (cond_array.get(((index_row, index_col1),(index_row, index_col2)),"") == "<"):
                            if tup[0]<tup[1]:
                                if tup not in sat_tuples:
                                        sat_tuples.append(tup)
                        else:
                            if tup not in sat_tuples:
                                sat_tuples.append(tup)
                C.add_satisfying_tuples(sat_tuples)
                csp.add_constraint(C)
            # Perform the same routine of checking but for vertical (e.g. columns) constraints
                col_var1 = var_array[index_col1][index_row]
                col_var2 = var_array[index_col2][index_row]
                C = Constraint("C[{0}][{1}][{2}][{3}]".format(index_col1, index_row, index_col2, index_row), [col_var1, col_var2])
                list_of_values = itertools.product(col_var1.cur_domain(),col_var2.cur_domain())
                sat_tuples = []
                for tup in list_of_values: # Checking conditions in between each value of the tuple (if there is a condition to begin with)
                    if tup[0] != tup[1]:
                        if tup not in sat_tuples:
                            sat_tuples.append(tup)
                C.add_satisfying_tuples(sat_tuples)
                csp.add_constraint(C)
    return csp, var_array
    

def futoshiki_csp_model_2(futo_grid):
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
    
    for index_row in range(len(var_array)):
                C = Constraint("C_r[{}]".format(index_row), var_array[index_row])
                lst = [v.cur_domain() for v in var_array[index_row]]
                list_of_values = itertools.product(*lst)
                sat_tuples = [] # satisfying tuples to add to constraint
                for tup in list_of_values:
                    if len(tup) != len(set(tup)):
                        continue
                    i = 0
                    # for i in range(len(tup)-1):
                    #     if tup[i] != tup[i+1]:
                    #         if cond_array.get(((index_row, i),(index_row, i+1)),"") == ">":
                    #             if tup[i]>tup[i+1]:
                    #                 if tup not in sat_tuples:
                    #                     sat_tuples.append(tup)
                    #         elif (cond_array.get(((index_row, i),(index_row, i+1)),"") == "<"):
                    #             if tup[i]<tup[i+1]:
                    #                 if tup not in sat_tuples:
                    #                     sat_tuples.append(tup)
                    #         else:
                    #             if tup not in sat_tuples:
                    #                 sat_tuples.append(tup)
                    while i != len(tup)-1: # Checking conditions in between each value of the tuple (if there is a condition to begin with)
                        if tup[i] == tup[i+1]:
                            break
                        if cond_array.get(((index_row, i),(index_row, i+1)),"") == ">":
                            if tup[i]<=tup[i+1]:
                                break
                                # if tup not in sat_tuples:
                                #     sat_tuples.append(tup)
                        elif (cond_array.get(((index_row, i),(index_row, i+1)),"") == "<"):
                            if tup[i]>=tup[i+1]:
                                break
                                # if tup not in sat_tuples:
                                #     sat_tuples.append(tup)
                        if i == len(tup)-2:
                            sat_tuples.append(tup)
                        i += 1
                C.add_satisfying_tuples(sat_tuples)
                csp.add_constraint(C)
            # Perform the same routine of checking but for vertical (e.g. columns) constraints
                C = Constraint("C_c[{}]".format(index_row), [var_array[j][index_row] for j in range(len(var_array))])
                lst = [var_array[j][index_row].cur_domain() for j in range(len(var_array))]
                list_of_values = itertools.product(*lst)
                sat_tuples = []
                for tup in list_of_values: # Checking conditions in between each value of the tuple (if there is a condition to begin with)
                    if len(tup) != len(set(tup)):
                        continue
                    if tup not in sat_tuples:
                        sat_tuples.append(tup)
                C.add_satisfying_tuples(sat_tuples)
                csp.add_constraint(C)
    return csp, var_array
   
