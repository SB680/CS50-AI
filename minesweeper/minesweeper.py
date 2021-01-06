import itertools
import random
import copy 

class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines

##a = Minesweeper()
##a.print() 
##print(a.nearby_mines((0,0)))  
##print (a.mines())
    
def adds(set1,set2):
    for element in set1:
        if element not in set2: 
            set2.add(element) 

class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count
        self.markedsafe = set() 
        self.markedmine = set() 

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        potentialmines = list(self.cells)[:];    
        for element in self.markedsafe: 
            potentialmines.remove(element) 
        if len(potentialmines) == self.count:
            #adds(potentialmines,self.markedmine)  
            return potentialmines 
       # if len(listhatexcludesknownmines) == len(self.cells) - len(self.markedmine):  
       #     return listhatexcludesknownmines
        return self.markedmine 
    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """ 
        potentialsafes = list(self.cells)[:];   
        for element in self.markedmine: 
            potentialsafes.remove(element) 
        if len(potentialsafes) == len(self.cells) - self.count:
            return potentialsafes
        
        #if len(potentialsafes) == len(self.cells) - len(self.known_mines()):
        #    print (len(potentialsafes)); print (len(self.cells)); print (len(self.known_mines())) 
        #    return potentialsafes 
        #elif count + len(withoutknownmines) == len(self.cells): 
        #    return withoutknownmines
        #print ("known mines: ",self.known_mines()) 
        return self.markedsafe   

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        self.markedmine.add(cell) 

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        self.markedsafe.add(cell)
    def __str__(self): 
        return(str(self.cells) + " count: " + str(self.count)) 



##a = Sentence({(1, 0), (1, 2)},0)
##print("KNown: ") 
##print(a.known_safes()) 
##sentence = Sentence({'A', 'B', 'C'},3)
##print ("AI")
##sentence.mark_mine('A')
##sentence.mark_mine('B') 
##print ("Known mines: ", sentence.known_mines())
##print ("Known safes: ", sentence.known_safes())

def issubset(set1,set2): #is set1 a subset of set 2?      
    for element in set1:
        if not element in set2:
            return False
    return True 
def disjoint(set1,set2):
    disj= set() 
    for element in set2:
        if element not in set1:
            disj.add(element)
    for element in set1:
        if element not in set2:
            disj.add(element) 
    return disj 

    
#set1 = {'A', 'B', 'C','E','F'}
#set2 = {'A', 'B', 'C','D'}
#print ("DISJOINT(IE ONLY IN ONE BUT NOT BOTH)",disjoint(set1,set2)) 
##print("testing issubset"); set1 = {'A','B','C'}; set2 = {'A','B','D','D'};
##
##print (issubset(set1,set2))

class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()
        
        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self,cell,count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """ 
        self.moves_made.add(cell)
        self.safes.add(cell)  
        neighbours = set() 
        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2): 
                if (i, j) == cell or (i,j) in self.safes:
                    continue 
                if 0 <= i < self.height and 0 <= j < self.width:
                    neighbours.add((i,j))   
        self.knowledge.append(Sentence(neighbours,count))

        l = len(self.knowledge)
        count = 0
        for sentence in self.knowledge:
            copycell = copy.deepcopy(sentence.cells)
            for cell in sentence.cells:
                if cell in self.safes:
                    copycell.remove(cell)
            sentence.cells = copycell 
        for i in range(l): 
            for j in range(l):
                if issubset(self.knowledge[i].cells,self.knowledge[j].cells) and not (i==j):  
                    disjoin = disjoint(self.knowledge[i].cells,self.knowledge[j].cells)
                    count1 = self.knowledge[i].count; count2 = self.knowledge[j].count 
                    #print ("disjoint: ", disjoin) 
                    self.knowledge.append(Sentence(disjoin,abs(count2-count1)))  
                
##        for i in range(l): 
##            for j in range(l): 
##                if issubset(self.knowledge[i].cells,self.knowledge[j].cells) and not (i==j):  
##                    self.knowledge.append(Sentence(disjoint(self.knowledge[i].cells,self.knowledge[j].cells),abs(self.knowledge[i].count-self.knowledge[j].count)))   

    #print ("cell: ",cell) 
        #for cell in neighbours: 
        #    print ("neighbour: ",cell) 
        #for sentence in self.knowledge: 
        #    print ("knowledge: ",sentence) 
##        l = len(self.knowledge)
##        count = 0 
##        for i in range(l):
##            count = max(self.knowledge[i].count,count) #the maximum count of mines 
##            for j in range(l):#can you go from i,l to make more efficient? 
##                if issubset(self.knowledge[i].cells,self.knowledge[j].cells) and not (i==j):  
##                    self.knowledge.append(Sentence(disjoint(self.knowledge[i].cells,self.knowledge[j].cells),abs(self.knowledge[i].count-self.knowledge[j].count))) 
##        for sentence in self.knowledge:
##            adds(sentence.known_mines(), self.mines)
        #for element in allcells:
        #    self.mines.remove(element)
        #    self.safes.remove(element)
        #for mine in self.
        #print("count: ",count)
##        if len(self.mines) == count: 
##            for cell in allcells:
##                if cell not in self.mines:
##                    self.safes.add(cell)

        for sentence in self.knowledge: 
            for element in sentence.known_safes():
                if element not in self.safes:
                    self.safes.add(element)

        for sentence in self.knowledge: 
            copycell = list(sentence.cells)[:] 
            for element in sentence.cells:
                if element in self.safes:
                    copycell.remove(element)
            sentence.cells = copycell 
 
        for sentence in self.knowledge:
            #print (sentence)
            #print ("KNOWN MINE: ", sentence.known_mines()) 
            for element in sentence.known_mines():
                if element not in self.mines:
                    self.mines.add(element) 
    def addknowledge2(self):
        allcells = set() 
        l = len(self.knowledge)
        count = 0 
        for i in range(l):
            count = max(self.knowledge[i].count,count) #the maximum count of mines 
            adds(self.knowledge[i].cells,allcells)
            for j in range(i,l):#can you go from i,l to make more efficient? 
                if issubset(self.knowledge[i].cells,self.knowledge[j].cells) and not (i==j): 
                    #print("yes")
                    #print ("disjoint: ", disjoint(self.knowledge[i].cells,self.knowledge[j].cells))  
                    self.knowledge.append(Sentence(disjoint(self.knowledge[i].cells,self.knowledge[j].cells),abs(self.knowledge[i].count-self.knowledge[j].count))) 
        for sentence in self.knowledge:
            adds(sentence.known_mines(), self.mines)
        #for mine in self.
        #print("count: ",count)
        if len(self.mines) == count: 
            for cell in allcells:
                if cell not in self.mines:
                    self.safes.add(cell)  
                    
    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes, 
        and self.moves_made, but should not modify any of those values.
        """
        for move in self.safes:
            if move not in self.moves_made:
                self.moves_made.add(move)
                return move 
        
    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        
        a = random.randint(0,self.height); b = random.randint(0,self.width);  
        while (a,b) in self.moves_made or (a,b) in self.moves_made:
            a = random.randint(0,self.height); b = random.randint(0,self.width);  

        self.moves_made.add((a,b))
        return (a,b) 
    
##a = MinesweeperAI()
###a.add_knowledge((2,2), 3)
##a.add_knowledge((0,1),1)
##a.add_knowledge((0,0),1)
##a.add_knowledge((0,2),1)
##a.add_knowledge((2,1),2)
####sen = Sentence({'A', 'B', 'D','R','E', 'Q'},5)
####a.knowledge.append(sen)
####a.knowledge.append(Sentence({'R'},1))  
####a.knowledge.append(Sentence({'A', 'B'},2))
####a.knowledge.append(Sentence({'E', 'Q'},2))
####a.add_knowledge()
##
####sen = Sentence({'A', 'B', 'D','R','E', 'Q','X','O','N'},6)
####a.knowledge.append(sen)
####a.knowledge.append(Sentence({'R'},1))  #DON'T USE MARKMINE OR MARKSAFE 
####a.knowledge.append(Sentence({'A', 'B'},2))
####a.knowledge.append(Sentence({'E', 'Q','O'},3))
##
##print ("knowledge: ")
##l = len(a.knowledge)
##copy = copy.deepcopy(a.knowledge)
##for i in range(l-1): 
##    for j in range(i+1,l):
##        if a.knowledge[i] == a.knowledge[j]:
##            if a.knowledge[i] in copy:
##                copy.remove(a.knowledge[i])
##a.knowledge = copy             
##for sentence in a.knowledge:
##    print(sentence)
##
##print ("Safes: ",a.safes)
##print ("Mines: ",a.mines)

##print("2nd time") 
##a.add_knowledge()
##for sentence in a.knowledge:
##    print(sentence)
##print("3rd time") 
##a.add_knowledge()
##for sentence in a.knowledge:
##    print(sentence)
