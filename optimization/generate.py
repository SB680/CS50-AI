import sys
import copy 
from crossword import *
#from schedule0 import * 
#from schedule1 import* 

class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }
        self.VARIABLES = [] 
        for key in self.domains.keys():
            self.VARIABLES.append(key)
        #print("CORSS: ",crossword.overlaps)
        self.overlaps = crossword.overlaps

        constraints = {self.overlaps[key] for key in self.overlaps if not self.overlaps[key] == None}
        
        print("variables: ",self.VARIABLES) 
        print("domains: ",self.domains)
        print("constraints: ",constraints) 
        
    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """ 
        for variable in self.VARIABLES:
            if variable not in assignment:
                return variable
        return None
    
    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        w, h = draw.textsize(letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        #print("overlaps: ",self.crossword.overlaps)
        overlaps = copy.deepcopy(self.crossword.overlaps) 
        for k in overlaps.keys():
            if overlaps[k] == None:
                del(self.crossword.overlaps[k])
        print("overlaps: ",self.crossword.overlaps)
		
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        #print("self.domains: ",self.domains)
        #dicti = {2:'TWO', 4:'FOUR', 10:'TEN', 6:'SIX', 9:'NINE', 1:'ONE', 7:'SEVEN', 5:'FIVE', 8:'EIGHT', 3:'THREE'}
        
        for k in self.domains.keys(): 
            for word in list(self.domains[k]) : 
                if not len(word) == k.length:
                    self.domains[k].remove(word) 
        #print("self.domains: ",self.domains)


    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """ 
        
        raise NotImplementedError


    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        pass 
        #if arcs == None:
        #    pass 
        #solution = backtrack(dict())
        #raise NotImplementedError

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        if len(assignment) == len(VARIABLES):
            return True
        return False 

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        """Checks to see if an assignment is consistent."""
        CONSTRAINTS = self.overlaps 
        for (x, y) in CONSTRAINTS.keys():
        # Only consider arcs where both are assigned
            if x not in assignment or y not in assignment or CONSTRAINTS[(x,y)] == None:
                continue
            num1 = CONSTRAINTS[(x,y)][0]; num2 = CONSTRAINTS[(x,y)][1]; 
            # If both have same value, then not consistent
            if not assignment[x][num1] == assignment[y][num2]: 
                return False 
        return True

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        raise NotImplementedError



    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        #print ("domains: ",self.domains)
     
        if len(assignment) == len(self.VARIABLES):
            return assignment

        # Try a new variable
        var = None 
        for variable in self.VARIABLES:
            if variable not in assignment:
                var = variable 
        #var = select_unassigned_variable(assignment)
        for value in self.domains[var]:
            new_assignment = assignment.copy()
            new_assignment[var] = value
            if self.consistent(new_assignment):
                result = self.backtrack(new_assignment)
                if result is not None:
                    return result
        return None


def main():

    # Check usage
    #print("solution: ",backtrack(dict()) ) 
    sys.argv = ['nu','data\structure0.txt','data\words0.txt']
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words) 
    creator = CrosswordCreator(crossword) 
    assignment = creator.solve() 

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


##a = Variable(1, 4, 'down', 4)
##word = 'FOUR'
##
##overlaps= {(Variable(1, 4, 'down', 4), Variable(4, 1, 'across', 4)): (3, 3), (Variable(0, 1, 'across', 3), Variable(0, 1, 'down', 5)): (0, 0),
##            (Variable(4, 1, 'across', 4),Variable(1, 4, 'down', 4)): (3, 3), (Variable(4, 1, 'across', 4), Variable(0, 1, 'down', 5)): (0, 4),                                                          
##           (Variable(0, 1, 'down', 5), Variable(0, 1, 'across', 3)): (0, 0), (Variable(0, 1, 'down', 5), Variable(4, 1, 'across', 4)): (4, 0)}
##domains= {Variable(1, 4, 'down', 4): {'FOUR', 'FIVE', 'NINE'}, Variable(0, 1, 'across', 3): {'TWO', 'TEN', 'SIX', 'ONE'},
##                Variable(4, 1, 'across', 4): {'FOUR', 'FIVE', 'NINE'}, Variable(0, 1, 'down', 5): {'SEVEN', 'THREE', 'EIGHT'}}
##
##dictvar = {}
##
##overlaps= [Variable(1, 4, 'down', 4)[3] == Variable(4, 1, 'across', 4)[3], Variable(0, 1, 'across', 3)[0] == Variable(0, 1, 'down', 5)[0],
##           Variable(4, 1, 'across', 4)[0] == Variable(0, 1, 'down', 5)[4]}
##
##for key in domains:
##    dictvar[key] = []
##    
##for key in overlaps:
##    #var1 = overlaps[key][0]; var 
##    var1 = key[0]; var2 = key[1]
##    num = overlaps[key][0]
##    #print("var1: ",var1, " var2: ",var2) 
##    #listd = list(domains[key]) #words for a particular variable in domains 
##    for word in domains[var1]: 
##  
##        
##    for word in domains[var2]:
##        #dictvar(domains[key[1]]).append(getchar(listd[1],word,num))
##        dictvar[var2].append(getchar(var2,word,num))
##
##print("dictvar: ",dictvar) 

if __name__ == "__main__":
    main()
