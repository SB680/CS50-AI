"""
Naive backtracking search without any heuristics or inference.
"""
from crossword import *

##VARIABLES = ["A", "B", "C", "D", "E", "F", "G"]
##
##CONSTRAINTS = [
##    ("A", "B"),
##    ("A", "C"),
##    ("B", "C"),
##    ("B", "D"),
##    ("B", "E"),
##    ("C", "E"),
##    ("C", "F"),
##    ("D", "E"),
##    ("E", "F"),
##    ("E", "G"),
##    ("F", "G")
##]
##
##
##def backtrack(assignment):
##    """Runs backtracking search to find an assignment."""
##
##    # Check if assignment is complete
##    if len(assignment) == len(VARIABLES):
##        return assignment
##
##    # Try a new variable
##    var = select_unassigned_variable(assignment)
##    for value in ["Monday", "Tuesday", "Wednesday"]:
##        new_assignment = assignment.copy()
##        new_assignment[var] = value
##        if consistent(new_assignment):
##            result = backtrack(new_assignment)
##            if result is not None:
##                return result
##    return None
##
##
##def select_unassigned_variable(assignment):
##    """Chooses a variable not yet assigned, in order."""
##    for variable in VARIABLES:
##        if variable not in assignment:
##            return variable
##    return None
##
##
##def consistent(assignment):
##    """Checks to see if an assignment is consistent."""
##    for (x, y) in CONSTRAINTS:
##
##        # Only consider arcs where both are assigned
##        if x not in assignment or y not in assignment:
##            continue
##
##        # If both have same value, then not consistent
##        if assignment[x] == assignment[y]:
##            return False
##
##    # If nothing inconsistent, then assignment is consistent
##    return True
##
##
##solution = backtrack(dict())
##print(solution)


VARIABLES = [Variable(1, 4, 'down', 4), Variable(4, 1, 'across', 4), Variable(0, 1, 'across', 3), Variable(0, 1, 'down', 5)]
 
CONSTRAINTS = {(Variable(1, 4, 'down', 4), Variable(4, 1, 'across', 4)): (3, 3), (Variable(0, 1, 'across', 3), Variable(0, 1, 'down', 5)): (0, 0),
            (Variable(4, 1, 'across', 4),Variable(1, 4, 'down', 4)): (3, 3), (Variable(4, 1, 'across', 4), Variable(0, 1, 'down', 5)): (0, 4),                                                          
           (Variable(0, 1, 'down', 5), Variable(0, 1, 'across', 3)): (0, 0), (Variable(0, 1, 'down', 5), Variable(4, 1, 'across', 4)): (4, 0)}

domains= {Variable(1, 4, 'down', 4): {'FOUR', 'FIVE', 'NINE'}, Variable(0, 1, 'across', 3): {'TWO', 'TEN', 'SIX', 'ONE'},
                Variable(4, 1, 'across', 4): {'FOUR', 'FIVE', 'NINE'}, Variable(0, 1, 'down', 5): {'SEVEN', 'THREE', 'EIGHT'}}

#value you map 'a' to can't be the same as that which you map 'b' to 


def backtrack(assignment):
    """Runs backtracking search to find an assignment."""

    # Check if assignment is complete
    if len(assignment) == len(VARIABLES):
        return assignment

    # Try a new variable
    var = select_unassigned_variable(assignment)
    for value in domains[var]:
        new_assignment = assignment.copy()
        new_assignment[var] = value
        if consistent(new_assignment):
            result = backtrack(new_assignment)
            if result is not None:
                return result
    return None


def select_unassigned_variable(assignment):
    """Chooses a variable not yet assigned, in order."""
    for variable in VARIABLES:
        if variable not in assignment:
            return variable
    return None


def consistent(assignment):
    """Checks to see if an assignment is consistent."""
    for (x, y) in CONSTRAINTS.keys():

        # Only consider arcs where both are assigned
        if x not in assignment or y not in assignment:
            continue

        num1 = CONSTRAINTS[(x,y)][0]; num2 = CONSTRAINTS[(x,y)][1]; 
        # If both have same value, then not consistent
        if not assignment[x][num1] == assignment[y][num2]: 
            return False

    # If nothing inconsistent, then assignment is consistent
    return True


solution = backtrack(dict())
print(solution)


