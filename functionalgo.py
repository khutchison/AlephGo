def printBoard(board):
	for row in range(len(board)):
		for col in range(len(board)):
			if row == (len(board) - 1):
				print(board[row][col][0])
			else:
				print(board[row][col][0] + " ", end = '')

#return [row, column] integer list as index for the next move
def getMove(a = int(input("Row: ")), b = int(input("Column: "))):
	return [a, b]

def makeBoard(size):
	return [[["+", 0] for column in range(size)] for row in range(size)]

def newGame(size):
	return {'board': makeBoard(size), 'currentPlayer': ["@", 0], 'otherPlayer': ["O", 0], 'groupList': {}, 'gameOver': False, 'availableGroups' = list(range(1, 20 * size))}

def placeStone(gameState, moveIndex):
	gameState['board'][moveIndex[0]][moveIndex[1]][0] = gameState['currentPlayer'][0]
	gameState['currentPlayer'][1] += 1
	return gameState

#complete this

def allyGroups():
	return friendGroups

def assignGroup(gameState, moveIndex):
	friendGroups = allyGroups(gameState, moveIndex)
	if friendGroups == []:
		gameState['board'][moveIndex[0]][moveIndex[1]][1] = gameState['availableGroups'][0]
		del gameState['availableGroups'][0]
	else:
		for row in gameState['board']:
			for col in gameState['board']:
				if col[1] in friendGroups:
					col[1] = gameState['availableGroups'][0]
		del gameState['availableGroups'][0]
		for group in friendGroups:
			gameState['availableGroups'].append(group)
			gameState['groupList'].remove(group)

	return gameState

def captureStones(gameState):
	return gameState

def switchPlayer(gameState):
	return {'board': gameState['board'], 'currentPlayer': gameState['otherPlayer'], 'otherPlayer': gameState['currentPlayer'], 'groupList': gameState['groupList'], 'gameOver': gameState['gameOver']}

def playStone(gameState, moveIndex):
	if isValid(gameState, moveIndex):
		return switchPlayer(captureStones(assignGroup(placeStone(gameState, moveIndex), moveIndex)))

def alephGo(SIZE = input("Game size: ")):
	gameState = newGame(SIZE)
	while gameState['gameOver'] == False:
		printBoard(gameState[board])
		gameState = playStone(gameState, getMove())
