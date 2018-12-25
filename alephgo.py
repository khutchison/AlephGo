#initialize score totals at 0
whitePoints = 0
blackPoints = 0

#get the game size
gameSize = int(input("Game Size > "))

# check out numpy 
# initialize the board, with "+" to represent an empty node, and 0 to mean no group
board = [[["+", 0] for i in range(gameSize)] for n in range(gameSize)]
myColor = "black"
stoneGroup = []
mySymbol = "@"
enemySymbol = "O"
gameOver = False
groupsAvailable = []
for x in range(100):
	groupsAvailable += [x]

# implement tracking of groups as state variables to save iterations?

def awardPoints(number): # award an arbitrary number of points, takes an integer argument
	if myColor == "black":
		blackPoints += number
	else:
		whitePoints += number

def switchPlayer(): # switch between the two players
	global myColor
	if myColor == "black":
		myColor = "white"
		mySymbol = "O"
		enemySymbol = "@"
	else:
		myColor = "black"
		mySymbol = "@"
		enemySymbol = "O"

def printBoard(): #print out the game board
	for i in range(gameSize):
		for n in range(gameSize):
			if n == (gameSize - 1):
				print(board[i][n][0])
			else:
				print(board[i][n][0] + " ", end = '')

def generateGroup(): #will return an unused group number and remove that number from the list of available group numbers
	myGroup = groupsAvailable[0]
	del groupsAvailable[0]
	return myGroup

def getGroup(index): # return the group of a specific stone. takes an index list argument
    return board[index[0]][index[1]][1] 

def massSetGroup(oldGroup, newGroup): # takes old group and what group to change it to 
	for i in board:
		for n in board: 
			if board[i][n][1] == oldGroup:
				board[i][n][1] = newGroup
	groupsAvailable += [oldGroup]

def assignGroup(row, column): #when a new stone is played, check whether it is next to allied or hostile groups and choose the appropriate response
	myAllies = adjacentAllies(row, column) # get a list of the board indices of any adjacent allies
	if myAllies == []: # if there are no adjacent stones, the played stone becomes a new group 
		board[row][column][1] = generateGroup()
	elif len(myAllies) == 1: # if there is exactly one adjacent ally, then:
		board[row][column][1] = board[myAllies[0][0]][myAllies[0][1]] # set the current stone's group to that of the adjacent ally. Should turn this into its own function? groupSet(index1, index2)
	else: #otherwise, if there is more than one adjacent ally:
		mergedGroup = newGroup() # create a new merged group identifier
		board[row][column][1] = mergedGroup # set the newly played stone to the merged group
		for index in myAllies: # for each stone indexed in myAllies, check its group
			massSetGroup(getGroup(myAllies[i]), mergedGroup)

def playStone(row, column):
	if board[row][column][0] != "+":
		print("Error: there is alreay a stone at those coordinates.")
	else:
		if myColor == "black":
			board[row][column][0] = "@"
			printBoard()
		else:
			board[row][column][0] = "O"
			printBoard()
		assignGroup(row, column)
		captureCheck(row, column)
		switchPlayer()

#remove stones, argument should be a list of board indices. Need separate capture method which should also award points. 
def removeStones(groupNumber):
	for i in board:
		for n in board:
			if board[i][n][1] == "groupNumber":
				board[i][n] = ["+", 0]
				awardPoints(1)

# get a list of indices adjacent to the target stone containing allied stones
def adjacentAllies(row, column):
	stoneList = []
	#need to add exceptions for edges and corners
	if board[row-1][column] == mySymbol:
		stoneList.append([row - 1, column])
	if board[row+1][column] == mySymbol:
		stoneList.append([row+1, column])
	if board[row][column+1] == mySymbol:
		stoneList.append([row, column+1])
		if board[row][column-1] == mySymbol:
			stoneList.append([row, column-1])
	return stoneList # return a list of the board indices of all adjacent allies

def adjacentHostiles(row, column):
	stoneList = []
	#need to add exceptions for edges and corners
	if board[row-1][column] == enemySymbol:
		stoneList.append([row - 1, column])
	if board[row+1][column] == enemySymbol:
		stoneList.append([row+1, column])
	if board[row][column+1] == enemySymbol:
		stoneList.append([row, column+1])
	if board[row][column-1] == enemySymbol:
		stoneList.append([row, column-1])
	return stoneList # return a list of the board indices of all adjacent enemy stones

def stoneLiberty(row, column):
	myStoneLiberty = False
	if board[row-1][column][0] == "+":
		myStoneLiberty = True
	elif board[row+1][column][0] == "+":
		myStoneLiberty = True
	elif board[row][column+1][0] == "+":
		myStoneLiberty = True
	elif board[row][column-1][0] == "+":
		myStoneLiberty = True
	return myStoneLiberty

def hasLiberty(groupNumber):
        myLiberty = False
        for i in board:
                for n in board:
                        if stoneLiberty(i, n) == True:
                                myLiberty = True
        return myLiberty

def captureCheck(row, column): # call this method to see if a newly played stone makes any captures
	enemyList = adjacentHostiles(row, column)
	while enemyList != []:
		enemyGroup = getGroup(enemyList[0])
		if hasLiberty(enemyGroup) == False:
			removeStones(enemyGroup)
		for n in enemyList:
			if getGroup(enemyList[n]) == enemyGroup:
				del enemyList[n]


# set up the main game loop 

printBoard()

def testPlayStone(row, column):
	if board[row][column][0] != "+":
		print("Error: there is alreay a stone at those coordinates.")
	else:
		if myColor == "black":
			board[row][column][0] = "@"
		else:
			board[row][column][0] = "O"
		assignGroup(row, column)
		captureCheck(row, column)


def testPlayStones():
        testPlayStone(3, 4)
        testPlayStone(3, 2)
        testPlayStone(2, 3)
        switchPlayer()
        playStone(3, 3)
        printBoard()
        
#while gameOver == False:
	#playStone(int(input("row > ")), int(input("column > ")))
