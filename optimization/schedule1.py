from constraint import *

from crossword import *

#from schedule0 import *

##problem = Problem()
##
### Add variables
##problem.addVariables(
##    ["A", "B", "C", "D", "E", "F", "G"],
##    ["Monday", "Tuesday", "Wednesday"]
##)
##
### Add constraints
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
##for x, y in CONSTRAINTS:
##    problem.addConstraint(lambda x, y: x != y, (x, y))
## #x -- the value to which x is mapped 
### Solve problem
##for solution in problem.getSolutions():
##    print(solution)

problem = Problem()

VARIABLES = ["var1","var2","var3","var4"]
#CONSTRAINTS = {("var1", "var2"): (3, 3), ("var3", "var4"): (0, 0), ("var2", "var3"): (0, 4),                                                          
#              ("var3", "var2"): (4, 0)}

CONSTRAINTS = {("var3", "var1"): (0, 0),
 ("var2", "var1"): (0, 4), ("var1",
             "var2"): (4, 0), ("var4", "var2"): (3, 3)}

domains =   {"var1": {'SEVEN', 'EIGHT', 'THREE', 'SIX', 'NINE', 'TWO', 'TEN', 'FIVE', 'ONE', 'FOUR'},
          "var2": {'SEVEN', 'EIGHT', 'THREE', 'SIX', 'NINE', 'TWO', 'TEN', 'FIVE', 'ONE', 'FOUR'},
           "var3": {'SEVEN', 'EIGHT', 'THREE', 'SIX', 'NINE', 'TWO', 'TEN', 'FIVE', 'ONE', 'FOUR'},
           "var4": {'SEVEN', 'EIGHT', 'THREE', 'SIX', 'NINE', 'TWO', 'TEN', 'FIVE', 'ONE', 'FOUR'}}

#domains= {"var1": {'FOUR', 'FIVE', 'NINE'}, "var3": {'TWO', 'TEN', 'SIX', 'ONE'},
#               "var2": {'FOUR', 'FIVE', 'NINE'}, "var4": {'SEVEN', 'THREE', 'EIGHT'}}

problem.addVariables(VARIABLES,domains)

# Add constraints

for (x, y) in CONSTRAINTS.keys():
    num1 = CONSTRAINTS[(x,y)][0]; num2 = CONSTRAINTS[(x,y)][1]; 
        # If both have same value, then not consistent
        #if not assignment[x][num1] == assignment[y][num2]: 
    problem.addConstraint(lambda x, y: x[num1] == y[num2], (x, y))
#this says the num1 position of the value to which x is mapped must equal ...; x is the value to which domains maps x 

# Solve problem
for solution in problem.getSolutions():
    print(solution)

# Add variables
#problem.addVariables(VARIABLES, ["ONEee","TWOee","THREE","FOURe","FIVEe","SIXrr","SEVEN","EIGHT","NINEe"]) #domains 

#problem.addVariables(VARIABLES, ["ONEee","TWOee","THREE","FOURe","FIVEe","SIXrr","SEVEN","EIGHT","NINEe"])

#domains= {Variable(1, 4, 'down', 4): {'FOUR', 'FIVE', 'NINE'}, Variable(0, 1, 'across', 3): {'TWO', 'TEN', 'SIX', 'ONE'},
#                Variable(4, 1, 'across', 4): {'FOUR', 'FIVE', 'NINE'}, Variable(0, 1, 'down', 5): {'SEVEN', 'THREE', 'EIGHT'}}

#VARIABLES = [Variable(1, 4, 'down', 4), Variable(4, 1, 'across', 4), Variable(0, 1, 'across', 3), Variable(0, 1, 'down', 5)]

#VARIABLES =  [Variable(0, 1, 'down', 5), Variable(4, 1, 'across', 4), Variable(0, 1, 'across', 3), Variable(1, 4, 'down', 4)]
