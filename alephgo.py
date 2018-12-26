# set the size of the game and create the board
gameSize = int(input("Game Size: "))
board = [[["+", 0] for column in range(gameSize)] for row in range(gameSize)]
groupList = [(i + 1) for i in range(gameSize * 10)]
gameOver = False

#keep track of the players by tile symbol and score 
player1 = ["@", 0]
player2 = ["O", 0]
currentPlayer = 1

# ----- game methods -----

def printBoard(): #print out the game board
	for i in range(gameSize):
		for n in range(gameSize):
			if n == (gameSize - 1):
				print(board[i][n][0])
			else:
				print(board[i][n][0] + " ", end = '')

def getSymbol():
	if currentPlayer == 1:
		return player1[0]
	else: 
		return player2[0]

def getGroup(index): 
	return board[index[0]][index[1]][1]

def isEmpty(row, column):
	if board[row][column][0] == "+":
		return True
	else: 
		return False

def isEdge(row, column): #determine whether the tile is on an edge
	if row < 1 or column < 1:
		return True
	if row == gameSize - 1 or column == gameSize - 1:
		return True
	else:
		return False

def adjacentAllies(row, column):
	allyList = []
	mySymbol = getSymbol()
	#if isEdge(row, column) == False:
	if board[row-1][column][0] == mySymbol:
		allyList.append([row - 1, column])
	if board[row+1][column][0] == mySymbol:
		allyList.append([row+1, column])
	if board[row][column+1][0] == mySymbol:
		allyList.append([row, column+1])
	if board[row][column-1][0] == mySymbol:
		allyList.append([row, column-1])
	#else: 
		# insert code for edge cases 
	return allyList

def newGroup():
	myGroup = groupList[0]
	del groupList[0]
	return myGroup

def mergeGroups(stonesList):
	groupsToMerge = []
	for index in stonesList:
		if (index not in groupsToMerge):
			groupsToMerge.append(getGroup(stonesList[index]))
	mergedGroup = newGroup()
	for row in board:
		for column in board:
			if board[row][column][1] in groupsToMerge:
				board[row][column][1] = mergedGroup
	for group in groupsToMerge:
		groupList.append(group)

def assignGroup(row, column):
	allyList = adjacentAllies(row, column)
	if len(allyList) == 0:
		board[row][column][1] = newGroup()
	elif len(allyList) == 1:
		board[row][column][1] = getGroup(allyList[0])
	else:
		allyList.append([row, column])
		mergeGroups(allyList)

def playStone(row, column):
	board[row][column][0] = getSymbol()
	assignGroup(row, column)

# -------- test methods below here --------
def printGroups():
	for i in range(gameSize):
		for n in range(gameSize):
			if n == (gameSize - 1):
				print(str(board[i][n][1]))
			else:
				print(str(board[i][n][1]) + " ", end = '')
# -------- test methods above here --------

def getMove():
	row = int(input("Row: "))
	column = int(input("Column: "))
	if isEmpty(row, column) == False:
		print("Error: there is already a stone at this index.")
		getMove()
	else: 
		playStone(row, column)
		printBoard()
		printGroups() # for test purposes ONLY!

# ----- game methods above -----

printBoard()

# ------ main game loop below -----
while gameOver == False:
	getMove()

