#import os
import sys
import random
import ast
#from dataclasses import dataclass

# Constant with size of rows/columns
_ARRAY_SIZE = 3

goalList =[[0,8,7],
       [6,5,4],
       [3,2,1]]

matrix_ledger = {'0':1} #add default init so that isn't considered as a state
fringe_list = []

def generate_number_list():
    number_list = list(range(0, _ARRAY_SIZE*3))
    random.shuffle(number_list) # it is shuffled in place
    return number_list


def create_puzzle(number_list=generate_number_list()):
    first_row = number_list[0:_ARRAY_SIZE*1]
    second_row = number_list[_ARRAY_SIZE*1:_ARRAY_SIZE*2]
    third_row = number_list[_ARRAY_SIZE*2:_ARRAY_SIZE*3]
    return [first_row, second_row, third_row]


def printMatrix(currentMatrix):
    """Print a list as a matrix."""
    # Goes through each row printing all the columns
    for x in range(0,_ARRAY_SIZE):
        print (currentMatrix[x][:])
    print("\n")


def add_to_matrix_history(aPuzzle):
    if(check_matrix_history(aPuzzle)):
        return 0 # If it already exists
    else:
        matrix_ledger[aPuzzle.matrixFingerprint] = 1
        return 1


def check_matrix_history(aPuzzle):
    return aPuzzle.matrixFingerprint in matrix_ledger #Returns true if it already exists


class puzzleType:
    """
    Class containing the methods and variables for the nodes generated of 
    the matrix.
    """    
    
    def __init__(self):
        self.displacedH = 0
        self.manDistH = 0
        self.totalH = 0
        self.parentNode = None
        self.currentMatrix = [[0,0,0],
                              [0,0,0],
                              [0,0,0]]
        self.matrixFingerprint = 0
        self.previousMoves = []


    def _setMatrix(self,provided_matrix):
        #print("Provided with: %s" %(provided_matrix) )
        if(isinstance(provided_matrix,str)):
            self.currentMatrix = create_puzzle(ast.literal_eval(provided_matrix))
        elif(isinstance(provided_matrix,list)):
            self.currentMatrix = provided_matrix
        else:
            raise ValueError('Provided matrix was not a list of numbers')
        self.matrixFingerprint = str(list(provided_matrix))

        if(not add_to_matrix_history(self)):
            print("In a recursive state aborting")
            exit()


    def _printMatrix(self):
        """Print a matrix object."""
        # Goes through each row printing all the columns
        for x in range(0, _ARRAY_SIZE):
            print (self.currentMatrix[x][:])
        print("\tThis matrix\'s value: %s\n"%(self.totalH))
        #print ("The total displaced heuristic is " + str(disHeur) + ", and the total Manhattan Distance is " + str(manDis))


    def _getManhattanDistance(self, anElement, currentX, currentY):
        """Calculate the Manhattan Distance heuristic from received list
           element to goal list. Return heuristic."""
        
        manDis = 0
        goalX = goalY = -1
        
        # Find the (x,y) coordinates of the element in the goal matrix.
        for x in range(0, _ARRAY_SIZE):
            # Try to find the element in the current row.
            try:
                # Find element in goalList and save coordinates.
                goalY = goalList[x].index(anElement)
                goalX = x
                # Break out of for loop.
                break
            except:
                # Index function of list will return an exception if failed.
                None 
        
        # If element wasn't found, print error message. 
        if goalX < 0 or goalY < -1:
            print ("Error in finding element in goal matrix.")
            return -1
        # Calculate Manhattan Distance for element.
        manDis = (abs(goalX - currentX) + abs(goalY - currentY))
        #print ("The manhattan distance of the element " + str(anElement) + " in the goal matrix is " + str(manDis))
        self.manDistH = manDis
        return manDis


    def _getHeuristics(self):
        """Get both heuristics from aList."""
        
        displacedHeuristic = 0
        displacedElement = disX = disY = -1
        cummulativeManDis = 0
        
        for x in range(0, _ARRAY_SIZE):
            for y in range(0, _ARRAY_SIZE):
                if self.currentMatrix[x][y] != goalList[x][y]:
                    #print ("Misplaced element found! -> " + str(self.currentMatrix[x][y]) + "!=" + str(goalList[x][y]))
                    displacedHeuristic += 1
                    disX = x
                    disY = y
                    displacedElement = self.currentMatrix[x][y]
                    cummulativeManDis += self._getManhattanDistance(displacedElement,disX,disY)
                    #print ("Current manDis " + str(cummulativeManDis))
        
        return displacedHeuristic, cummulativeManDis
    

    def _assignHeuristicsToNode(self):
        """Finds the heuristics and saves it to the current node."""
        disH = mdH = 0
        
        disH, mdH = self._getHeuristics()
        self.displacedH = disH
        self.manDistH = mdH
        self.totalH = disH + mdH
    
    
    def _checkGoal(self):
        """Check if current list is the goal state."""
        
        for x in range(0, _ARRAY_SIZE):
            for y in range(0, _ARRAY_SIZE):
                if self.currentMatrix[x][y] != goalList[x][y]:
                    return False
        print("found goal")        
        return True
    

    def _cloneMatrix(self):
        """Clone current matrix to new puzzleType node and return. Used
           for creating new children nodes."""
        tempNode = puzzleType()
        
        for x in range(0, _ARRAY_SIZE):
            tempNode.currentMatrix[x] = self.currentMatrix[x][:]
            
        return tempNode
    

    def _generatePossibleStates(self):
        """Generate all possible moves in the current puzzle."""

        zeroX, zeroY = self._getZeroPosition()
        tempX = tempY = 0
        listNodesGenerated = []
        
        if zeroX > 0: # if empty is not on the left-most side
            tempNode1 = self._cloneMatrix()
            tempNode1.parent = self
            tempNode1.currentMatrix[zeroX][zeroY] = self.currentMatrix[zeroX-1][zeroY]
            tempNode1.currentMatrix[zeroX-1][zeroY] = self.currentMatrix[zeroX][zeroY]
            tempNode1._assignHeuristicsToNode()
            listNodesGenerated.append(tempNode1)
        if zeroX < (_ARRAY_SIZE - 2): # if empty is not on the right-most side
            tempNode2 = self._cloneMatrix()
            tempNode2.parent = self
            tempNode2.currentMatrix[zeroX][zeroY] = self.currentMatrix[zeroX+1][zeroY]
            tempNode2.currentMatrix[zeroX+1][zeroY] = self.currentMatrix[zeroX][zeroY]
            tempNode2._assignHeuristicsToNode()
            listNodesGenerated.append(tempNode2)
        if zeroY > 0: # if empty is not on the bottom side
            tempNode3 = self._cloneMatrix()
            tempNode3.parent = self
            tempNode3.currentMatrix[zeroX][zeroY] = self.currentMatrix[zeroX][zeroY-1]
            tempNode3.currentMatrix[zeroX][zeroY-1] = self.currentMatrix[zeroX][zeroY]
            tempNode3._assignHeuristicsToNode()
            listNodesGenerated.append(tempNode3)
        if zeroY < (_ARRAY_SIZE - 2): # if empty is not on the top side
            tempNode4 = self._cloneMatrix()
            tempNode4.parent = self
            tempNode4.currentMatrix[zeroX][zeroY] = self.currentMatrix[zeroX][zeroY+1]
            tempNode4.currentMatrix[zeroX][zeroY+1] = self.currentMatrix[zeroX][zeroY]
            tempNode4._assignHeuristicsToNode()
            listNodesGenerated.append(tempNode4)
        
        return listNodesGenerated
    

    def _getZeroPosition(self):
        """Get the x and y coordinates of the zero tile."""
        for x in range(0, _ARRAY_SIZE):
            for y in range(0, _ARRAY_SIZE):
                if self.currentMatrix[x][y] == 0:
                    return x, y
        
        return -1,-1    
        

def getListFromUser():
    """Get test list from user input."""
    print ("Enter the test puzzle matrix (9 numbers, hit enter after each one): ")
    aList = [[0,0,0],
             [0,0,0],
             [0,0,0]]
    
    for x in range(0, _ARRAY_SIZE):
        for y in range(0, _ARRAY_SIZE):
            aList[x][y] = int(input())
    
    printMatrix(aList)
    return aList
    

def getGoalListFromUser():
    """Get goal list from user input."""
    print ("Enter the goal puzzle matrix (9 numbers, from 0-8, \n hit enter after each one): ")
    
    for x in range(0, _ARRAY_SIZE):
        for y in range(0, _ARRAY_SIZE):
            goalList[x][y] = int(input())
    
    printMatrix(goalList)    


def determine_best_move(listNodesGenerated):
    #print("List of nodes Generated: %s"%(listNodesGenerated))
    options_by_value = sorted(listNodesGenerated, key=lambda obj: obj.totalH)
    options_by_value.append(fringe_list) #Add existing fringe_list containing unattempted states
    x = 0
    while(check_matrix_history(options_by_value[x])): #enter loop if true
        x = x + 1
    #print("selected: %s"%(options_by_value[x].currentMatrix))
    fringe_list.append(options_by_value[:x:-1][::-1]) #slice python lower-bound exclusive and then reverse the order
    return options_by_value[x] #Current selection is left out of fringe_list
    

def start_solving(puzzle):
    if(puzzle._checkGoal()):
        return 1
    else:
        aListOfNodes = puzzle._generatePossibleStates()
        next_move = determine_best_move(aListOfNodes)
        puzzle._setMatrix(next_move.currentMatrix)

        # print("Printing next move possibilities: ")
        # for x in range(0, len(aListOfNodes)):
        #     tempNode = aListOfNodes.pop()
        #     tempNode._printMatrix()

        start_solving(puzzle)


def main():
    init_puzzle = puzzleType()

    arg_length = len(sys.argv)

    if (arg_length > 1):
        print("Starting Import with the following parameters: " + str(sys.argv))
        try:
            init_puzzle._setMatrix(sys.argv[1])
        except ValueError:
            print("Was not provided a list of integers\nAsking user to type in puzzle starting from top left")
            init_puzzle._setMatrix(getListFromUser())
    else:
        init_puzzle._setMatrix(create_puzzle())
    printMatrix(init_puzzle.currentMatrix)
    print("Puzzle recieved, solving problem")

    if(start_solving(init_puzzle)):
        print("Solution Found after %s attempts"%(len(matrix_ledger)))


if __name__ == "__main__":
    main()
