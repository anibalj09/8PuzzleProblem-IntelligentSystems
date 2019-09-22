#import os
import sys
#from dataclasses import dataclass

# Constant with size of rows/columns
_ARRAY_SIZE = 3

goalList =[[9,8,7],
		   [6,5,4],
		   [3,2,1]]


class puzzleType:
	def __init__(self):
		


def printMatrix(aList):
	"""Print a list as a matrix."""
	
	#print ("\n")
	# Goes through each row printing all the columns
	for x in range(0,_ARRAY_SIZE):
		print (aList[x][:])
	print ("\n")

def getManhattanDistance(anElement, currentX, currentY):
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
	print ("The manhattan distance of the element " + str(anElement) + " in the goal matrix is " + str(manDis))
	return manDis


def getHeuristics(aList):
	"""Get both heuristics from aList."""
	
	displacedHeuristic = 0
	displacedElement = disX = disY = -1
	cummulativeManDis = 0
	
	for x in range(0, _ARRAY_SIZE):
		for y in range(0, _ARRAY_SIZE):
			if aList[x][y] != goalList[x][y]:
				print ("Misplaced element found! -> " + str(aList[x][y]) + "!=" + str(goalList[x][y]))
				displacedHeuristic += 1
				disX = x
				disY = y
				displacedElement = aList[x][y]
				cummulativeManDis += getManhattanDistance(displacedElement,disX,disY)
				#print ("Current manDis " + str(cummulativeManDis))
	
	return displacedHeuristic, cummulativeManDis

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

def generatePossibleStates(aList):
	"""Generate all possible moves in the current puzzle."""

def compareMatrixes(aList):
	"""Check if current list is the goal state."""
	
	for x in range(0, _ARRAY_SIZE):
		for y in range(0, _ARRAY_SIZE):
			if aList[x][y] != goalList[x][y]:
				return False	
	
	return True
	
	
def main():
	aList = [[1,2,3],
			 [4,5,6],
			 [7,8,9]]
	
	#disHeur, manDis = getHeuristics(aList)
	#print ("The total displaced heuristic is " + str(disHeur) + ", and the total Manhattan Distance is " + str(manDis))
			 

if __name__ == "__main__":
    main()
