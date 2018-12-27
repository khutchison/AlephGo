# set the size of the game and create the board
gameSize = int(input("Game Size: "))
board = [[["+", 0] for column in range(gameSize)] for row in range(gameSize)]
groupList = [(i + 1) for i in range(gameSize * 100)]
gameOver = False

#keep track of the players by tile symbol and score 
player1 = ["@", 0]
player2 = ["O", 0]
currentPlayer = 1

# ----- game methods -----

def printScore():
	if currentPlayer == 1:
		print(player1[1])
	else:
		print(player2[1])

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

def getEnemySymbol():
	if currentPlayer == 1:
		return player2[0]
		#print("Got enemy symbol! " + player2[0]) #TESTPRINT
	else: 
		return player1[0]
		#print("Got enemy symbol! " + player1[0]) #TESTPRINT

def getGroup(index):
	#print(board[index[0]][index[1]][1]) 
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
	if (row > 0) and (board[row-1][column][0] == mySymbol):
		allyList.append([row - 1, column])
	if (row < gameSize - 1) and (board[row+1][column][0] == mySymbol):
		allyList.append([row+1, column])
	if (column < gameSize) and (board[row][column+1][0] == mySymbol):
		allyList.append([row, column+1])
	if (column > 0) and (board[row][column-1][0] == mySymbol):
		allyList.append([row, column-1])
	#else: 
		# insert code for edge cases 
	return allyList

def newGroup():
	myGroup = groupList[0]
	del groupList[0]
	return myGroup

def mergeGroups(stonesList, row, column):
	groupsToMerge = []
	myGroup = None
	for i in stonesList:
		myGroup = getGroup(i)
		if myGroup not in groupsToMerge:
			groupsToMerge.append(myGroup)
	mergedGroup = newGroup()
	for r in range(gameSize):
		for c in range(gameSize):
			if board[r][c][1] in groupsToMerge:
				board[r][c][1] = mergedGroup
	board[row][column][1] = mergedGroup
	#for group in groupsToMerge:
		#groupList.append(group)

def assignGroup(row, column):
	allyList = adjacentAllies(row, column)
	if len(allyList) == 0:
		board[row][column][1] = newGroup()
	elif len(allyList) == 1:
		board[row][column][1] = getGroup(allyList[0])
	else:
		mergeGroups(allyList, row, column)
		
		#for i in range(len(allyList)):
			#print(allyList[i][1])
	#print(len(allyList)) # TESTPRINT
def adjacentEnemies(row, column):
	enemyList = []
	enemySymbol = getEnemySymbol()
	#if isEdge(row, column) == False:
	if (row > 0) and (board[row-1][column][0] == enemySymbol):
		enemyList.append([row - 1, column])
	if (row < gameSize - 1) and (board[row+1][column][0] == enemySymbol):
		enemyList.append([row+1, column])
	if (column < gameSize - 1) and (board[row][column+1][0] == enemySymbol):
		enemyList.append([row, column+1])
	if (column > 0) and (board[row][column-1][0] == enemySymbol):
		enemyList.append([row, column-1])
	#else: 
		# insert code for edge cases 
	#print("Enemy list length: " + str(len(enemyList))) # TESTPRINT
	return enemyList

def hasLiberty(row, column):
	if (board[row-1][column][0] == "+") and (row > 0):
		return True
	elif (board[row+1][column][0] == "+") and (row < gameSize - 1):
		return True
	elif (board[row][column+1][0] == "+") and (column < gameSize + 1):
		return True
	elif (board[row][column-1][0] == "+") and (column > 0):
		return True
	else:
		return False

def groupHasLiberty(groupNumber):
	myLiberty = False
	for i in range(gameSize):
		if myLiberty == True:
			break
		else: 
			for n in range(gameSize):
				if (hasLiberty(i, n) == True) and getGroup([i, n]) == groupNumber:
					print("Found a liberty! groupHasLiberty")
					myLiberty = True
					break
	return myLiberty

def awardPoints(number):
	if currentPlayer == 1:
		player1[1] += number
	else:
		player2[1] += number
	printScore() #TESTPRINT

def removeStone(row, column):
	board[row][column] = ["+", 0]
	awardPoints(1)

def groupCapture(groupNumber):
	for r in range(gameSize):
		for c in range(gameSize):
			if board[r][c][1] == groupNumber:
				removeStone(r, c)

def captureCheck(row, column):
	myEnemies = adjacentEnemies(row, column)
	enemyGroups = []
	for i in range(len(myEnemies)):
		r = myEnemies[i][0]
		c = myEnemies[i][1]
		enemyGroups.append(board[r][c][1])
	for n in enemyGroups:
		if groupHasLiberty(n) == False:
			groupCapture(n)

def playStone(row, column):
	board[row][column][0] = getSymbol()
	assignGroup(row, column)
	captureCheck(row, column)
	#allyList = adjacentAllies(row, column)
	#print("allyList: " + str(len(allyList))) # TESTPRINT

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

def switchPlayer():
	global currentPlayer
	if currentPlayer == 1:
		currentPlayer = 2
	else:
		currentPlayer = 1

# ----- game methods above -----

printBoard()

# ------ main game loop below -----
while gameOver == False:
	getMove()
	switchPlayer()

