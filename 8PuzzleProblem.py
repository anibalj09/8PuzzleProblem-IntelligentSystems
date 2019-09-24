#import os
import sys
import random
#from dataclasses import dataclass

# Constant with size of rows/columns
_ARRAY_SIZE = 3

goalList =[[0,8,7],
		   [6,5,4],
		   [3,2,1]]

def generate_number_list():
	number_list = list(range(0, _ARRAY_SIZE*3))
	random.shuffle(number_list) # it is shuffled in place
	return number_list

def create_puzle():
    number_list = generate_number_list()
    first_row = number_list[0:_ARRAY_SIZE*1]
    second_row = number_list[_ARRAY_SIZE*1:_ARRAY_SIZE*2]
    third_row = number_list[_ARRAY_SIZE*2:_ARRAY_SIZE*3]
    return [first_row, second_row, third_row]

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
	
	def _printMatrix(self):
		"""Print a list as a matrix."""
		
		#print ("\n")
		# Goes through each row printing all the columns
		for x in range(0,_ARRAY_SIZE):
			print (self.currentMatrix[x][:])
		print ("\n")

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
	
	
	def _compareMatrixes(self):
		"""Check if current list is the goal state."""
		
		for x in range(0, _ARRAY_SIZE):
			for y in range(0, _ARRAY_SIZE):
				if self.currentMatrix[x][y] != goalList[x][y]:
					return False		
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
		
		if zeroX > 0:
			tempNode1 = self._cloneMatrix()
			tempNode1.parent = self
			tempNode1.currentMatrix[zeroX][zeroY] = self.currentMatrix[zeroX-1][zeroY]
			tempNode1.currentMatrix[zeroX-1][zeroY] = self.currentMatrix[zeroX][zeroY]
			tempNode1._assignHeuristicsToNode()
			listNodesGenerated.append(tempNode1)
		if zeroX < (_ARRAY_SIZE - 2):
			tempNode2 = self._cloneMatrix()
			tempNode2.parent = self
			tempNode2.currentMatrix[zeroX][zeroY] = self.currentMatrix[zeroX+1][zeroY]
			tempNode2.currentMatrix[zeroX+1][zeroY] = self.currentMatrix[zeroX][zeroY]
			tempNode2._assignHeuristicsToNode()
			listNodesGenerated.append(tempNode2)
		if zeroY > 0:
			tempNode3 = self._cloneMatrix()
			tempNode3.parent = self
			tempNode3.currentMatrix[zeroX][zeroY] = self.currentMatrix[zeroX][zeroY-1]
			tempNode3.currentMatrix[zeroX][zeroY-1] = self.currentMatrix[zeroX][zeroY]
			tempNode3._assignHeuristicsToNode()
			listNodesGenerated.append(tempNode3)
		if zeroY < (_ARRAY_SIZE - 2):
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

	
	
def main():
	aNode = puzzleType() 
	#aNode.currentMatrix = [[1,2,3],
	#					   [4,5,6],
	#					   [7,8,0]]
	aNode.currentMatrix = create_puzle()
						   
	aListOfNodes = aNode._generatePossibleStates()
	for x in range(0, len(aListOfNodes)):
		tempNode = aListOfNodes.pop()
		tempNode._printMatrix()
	
	#disHeur, manDis = getHeuristics(aList)
	#print ("The total displaced heuristic is " + str(disHeur) + ", and the total Manhattan Distance is " + str(manDis))
			 

if __name__ == "__main__":
    main()
