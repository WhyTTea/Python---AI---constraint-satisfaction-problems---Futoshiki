#Look for #IMPLEMENT tags in this file. These tags indicate what has
#to be implemented to complete problem solution.  

'''This file will contain different constraint propagators to be used within 
   bt_search.

   propagator == a function with the following template
      propagator(csp, newly_instantiated_variable=None)
           ==> returns (True/False, [(Variable, Value), (Variable, Value) ...]

      csp is a CSP object---the propagator can use this to get access
      to the variables and constraints of the problem. The assigned variables
      can be accessed via methods, the values assigned can also be accessed.

      newly_instaniated_variable is an optional argument.
      if newly_instantiated_variable is not None:
          then newly_instantiated_variable is the most
           recently assigned variable of the search.
      else:
          progator is called before any assignments are made
          in which case it must decide what processing to do
           prior to any variables being assigned. SEE BELOW

       The propagator returns True/False and a list of (Variable, Value) pairs.
       Return is False if a deadend has been detected by the propagator.
       in this case bt_search will backtrack
       return is true if we can continue.

      The list of variable values pairs are all of the values
      the propagator pruned (using the variable's prune_value method). 
      bt_search NEEDS to know this in order to correctly restore these 
      values when it undoes a variable assignment.

      NOTE propagator SHOULD NOT prune a value that has already been 
      pruned! Nor should it prune a value twice

      PROPAGATOR called with newly_instantiated_variable = None
      PROCESSING REQUIRED:
        for plain backtracking (where we only check fully instantiated 
        constraints) 
        we do nothing...return true, []

        for forward checking (where we only check constraints with one
        remaining variable)
        we look for unary constraints of the csp (constraints whose scope 
        contains only one variable) and we forward_check these constraints.

        for gac we establish initial GAC by initializing the GAC queue
        with all constaints of the csp


      PROPAGATOR called with newly_instantiated_variable = a variable V
      PROCESSING REQUIRED:
         for plain backtracking we check all constraints with V (see csp method
         get_cons_with_var) that are fully assigned.

         for forward checking we forward check all constraints with V
         that have one unassigned variable left

         for gac we initialize the GAC queue with all constraints containing V.
		 
		 
var_ordering == a function with the following template
    var_ordering(csp)
        ==> returns Variable 

    csp is a CSP object---the heuristic can use this to get access to the
    variables and constraints of the problem. The assigned variables can be
    accessed via methods, the values assigned can also be accessed.

    var_ordering returns the next Variable to be assigned, as per the definition
    of the heuristic it implements.
   '''

def prop_BT(csp, newVar=None):
    '''Do plain backtracking propagation. That is, do no 
    propagation at all. Just check fully instantiated constraints'''
    
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
    '''Do forward checking. That is check constraints with 
       only one uninstantiated variable. Remember to keep 
       track of all pruned (variable,value) pairs and return '''
    pruned = []
    if not newVar: # no newVar given by the user
        constraints = csp.get_all_cons()
    else: # newVar given by the user
        constraints = csp.get_cons_with_var(newVar)
    for C in constraints: # list of all C's in CSP
        if C.get_n_unasgn() != 1: # return # of unassigned variables in this particular C
                continue
        else: # the case where the number of unassigned variables in the constraint's scope == 1        
            var = C.get_unasgn_vars()[0]
            for value in var.cur_domain():
                values_for_check = []
                for check_var in C.get_scope(): #re-assemble the list of values in the same order as variables are for the check method
                    if check_var != var:
                        values_for_check.append(check_var.get_assigned_value()) # follow the order of var when appending val for each var
                    else:
                        values_for_check.append(value) # found our unassigned var, so insert our guess for its value
                if C.check(values_for_check) == False: # constraints fails => prune the value 
                    var.prune_value(value)
                    pruned.append((var, value))
            if var.cur_domain_size() == 0: # DWO/dead-end condition
                return (False, pruned)
    return (True, pruned) 

def prop_GAC(csp, newVar=None):
    '''Do GAC propagation. If newVar is None we do initial GAC enforce 
       processing all constraints. Otherwise we do GAC enforce with
       constraints containing newVar on GAC Queue'''
    pruned = []
    filtered_cons = []
    if not newVar: # no newVar given by the user
        constraints = csp.get_all_cons()
    else: # newVar given by the user
        constraints = csp.get_cons_with_var(newVar)
    while len(constraints) != 0: # while the queue is not empty
        C = constraints.pop(0) 
        if C.get_n_unasgn() == 0: # return # of unassigned variables in this particular C. If it's completely assigned - skip unneccesary work
                continue
        else:
            for var in C.get_scope(): # find all vars this contraints covers
                for value in var.cur_domain(): # find all values available to iterate over in the unassigned var
                    if C.has_support(var, value) == False: # perform the check
                        var.prune_value(value)
                        pruned.append((var, value))
                        constraints.extend(csp.get_cons_with_var(var))
                if var.cur_domain_size() == 0: # DWO/dead-end condition
                    return (False, pruned)
    return (True, pruned)

def ord_mrv(csp):
    ''' return variable according to the Minimum Remaining Values heuristic '''
    min = (None, float('inf'))
    for var in csp.get_all_unasgn_vars(): # pull all unassigned vars
        if var.cur_domain_size() < min[1]: # pull all available values for each var to tail up the count
            min = (var, var.cur_domain_size()) 
    return min[0]

	