import numpy as np
from copy import deepcopy


class TTTboard():
	def __init__(self):
		self.grid = np.zeros((3,3), int)
		self.symbols = {'o': 2, 'x': 1, ' ': 0}
		self.gameOver = False
		self.winner = None


	def checkForWin(self, player):

		assert player == 'o' or player == 'x'

		target = np.ones(3, int) * self.symbols[player]

		if (self.grid[0] == target).all() or (self.grid[1] == target).all() or (self.grid[2] == target).all() or (self.grid.T[0] == target).all() or (self.grid.T[1] == target).all() or (self.grid.T[2] == target).all():
			self.gameOver = True
			self.winner = player


		if (np.diag(self.grid) == target).all() or (np.diag(np.fliplr(self.grid)) == target).all():
			self.gameOver = True
			self.winner = player



	def over(self):
		if not self.gameOver and np.min(self.grid) > 0:
			self.gameOver = True


	def isValidMove(self, (i,j)):
		return self.grid[i,j] == 0

	def makeMove(self, player, mv):
		(i, j) = mv
		if not self.grid[i,j]:
			self.grid[i,j] = self.symbols[player]

		else:
			print('invalid move')
			sys.exit(1)

		return grid


	def getGrid(self, player):
		#each player wants to see themselves as 1 and the opponent as 2
		if self.symbols[player] == 1:
			return self.grid

		ii, jj = np.where(self.grid > 0)
		tempGrid = deepcopy(self.grid)
		tempGrid[ii, jj] = 3 - self.grid[ii, jj]

		return tempGrid




	@staticmethod
	def hashGrid(grid):

		'''
		Creates a unique hash code for a given board configuration.
		This is done by converting the board values (0 for empty, 1 for cross, 2 for circle) into an integer in base 3

		INPUT
		grid:   3x3 numpy array containing a valid tic-tac-toe board

		RETURNS
		The hash value (in base 10)

		'''

		return int(str(grid[2,2]) + str(grid[2,1]) + str(grid[2,0]) + str(grid[1,2]) + str(grid[1,1]) + str(grid[1,0]) + str(grid[0,2]) + str(grid[0,1]) + str(grid[0,0]) , 3)

	@staticmethod
	def unhash(nr):
		grid = np.zeros((3,3), int)
		pos = [(0,0), (0,1), (0,2), (1,0), (1,1), (1,2), (2,0), (2,1), (2,2)]
		#grid[0,0] = hash % 3
		cnt = 0

		while nr > 0:
			grid[pos[cnt]] = nr % 3

			nr = nr / 3
			cnt += 1


		return grid



class Player():
	def __init__(self, symbol):
		assert symbol == 'o' or symbol == 'x'
		self.symbol = symbol


	def getValidMoves(grid):
		[xx, yy] = np.where(grid == 0)


		mv = []
		for (x,y) in zip (xx, yy):
			mv.append((x,y))

		return mv




	def haveIseenIt(grid, hashes):
		'''
		Determine if a particular board configuration (or any equivalent to it due to symmetry) has been observed before

		INPUTS:
		grid:   3x3 numpy array containing a valid tic-tac-toe board
		hashes: set of all the hash values of all the board configurations that have been observed

		RETRUNS:
		grid:


		'''

		if hashGrid(grid) in hashes:
			return grid, 0


		if hashGrid(np.flipud(grid)) in hashes:
			return np.flipud(grid), 1


		if hashGrid(np.fliplr(grid)) in hashes:
			return np.fliplr(grid), 2

		if hashGrid(np.flipud(np.fliplr(grid))) in hashes:
			return np.flipud(np.fliplr(grid)), 3


		grid90 = np.rot90(grid)

		if hashGrid(grid90) in hashes:
			return grid90, 4


		if hashGrid(np.fliplr(grid90)) in hashes:
			return np.fliplr(grid90), 5

		if hashGrid(np.flipud(grid90)) in hashes:
			return np.flipud(grid90), 6


		grid270 = np.rot90(np.rot90(grid90))

		if hashGrid(grid270) in hashes:
			return grid270, 7

		return grid, -1




def backToNormal(grid, code):
	if code < 1:
		return grid

	if code == 1:
		return np.flipud(grid)


	if code == 2:
		return np.fliplr(grid)


	if code == 3:
		return np.fliplr(np.flipud(grid))

	if code == 4:
		return np.rot90(np.rot90(np.rot90(grid)))

	if code == 5:
		return np.rot90(np.rot90(np.rot90(np.fliplr(grid))))


	if code == 6:
		return np.rot90(np.rot90(np.rot90(np.fliplr(grid))))



	if code == 7:
		return np.rot90(grid)







def removeRedundantMoves(grid, possibleMoves):
	if len(possibleMoves) < 2:
		return possibleMoves

	seenStates = set()

	corners = {(0,0), (0,2), (2,0), (2,2)}


	corners = list(corners.intersection(set(possibleMoves)))

	N = len(corners)
	if N:

		tobedel = []
		for i in range(N):
			c1 = corners[i]

			if haveIseenIt(makeMove(deepcopy(grid), 1, c1), seenStates)[1] > 0:
				tobedel.append(c1)
			else:
				seenStates.add(hashGrid(makeMove(deepcopy(grid), 1, c1)))

		for i in sorted(tobedel, reverse=True):
			del possibleMoves[possibleMoves.index(i)]


	seenStates = set()

	corners = {(0,1), (1,0), (1,2), (2,1)}


	corners = list(corners.intersection(set(possibleMoves)))

	N = len(corners)
	if N:

		tobedel = []
		for i in range(N):
			c1 = corners[i]

			if haveIseenIt(makeMove(deepcopy(grid), 1, c1), seenStates)[1] > 0:
				tobedel.append(c1)
			else:
				seenStates.add(hashGrid(makeMove(deepcopy(grid), 1, c1)))

		for i in sorted(tobedel, reverse=True):
			del possibleMoves[possibleMoves.index(i)]



	return possibleMoves






def bestMoveRnd(hh, possibleMoves, stateAndMove):

	allpossible = set(range(len(possibleMoves)))

	triedSoFar = sorted([k[1] for k in stateAndMove if k[0] == hh])

	#print allpossible
	#print triedSoFar
	#print



	if len(triedSoFar) == len(allpossible):
		#all have been tested at least once
		stats = [stateAndMove[k] for k in stateAndMove if k[0] == hh]

		attempt = []
		success = []

		for stat in stats:
			attempt.append(stat[0])
			success.append(np.maximum(stat[1], 0.0))

		rates = np.array(success) / np.array(attempt)


		if np.sum(rates) == 0.0:
			rates = np.ones((len(allpossible),), float) / len(allpossible)

		else:
			rates = rates / np.sum(rates)


	else:
		#those tried choose as before


		probCoveredByTried = len(triedSoFar) / float(len(allpossible))
		nrNotTried = len(allpossible.difference(triedSoFar))


		rates = np.zeros((len(allpossible),), float)

		ind = []
		temprates = []
		for move in sorted(allpossible):
			if move in triedSoFar:
				(aa, ss) = stateAndMove[(hh, move)]

				ind.append(move)
				temprates.append(np.maximum(ss, 0.0) / float(aa))

			else:
				rates[move] = (1 - probCoveredByTried) / float(nrNotTried)

		temprates = np.array(temprates)

		if np.sum(temprates) == 0.0:
			temprates = np.ones((len(allpossible) - nrNotTried), float) / float(len(allpossible) - nrNotTried)
		else:
			temprates = temprates / np.sum(temprates)

		for kounter, ii in enumerate(ind):
			rates[ii] = probCoveredByTried * temprates[kounter]



	return np.random.choice(np.arange(len(allpossible)), size = 1, p = rates)




def bestMove(hh, possibleMoves, stateAndMove):

	allpossible = set(range(len(possibleMoves)))

	triedSoFar = sorted([k[1] for k in stateAndMove if k[0] == hh])


	print possibleMoves

	print triedSoFar
	print allpossible

	assert len(triedSoFar) == len(allpossible)
	#all have been tested at least once
	stats = [stateAndMove[k] for k in stateAndMove if k[0] == hh]

	print stats

	attempt = []
	success = []

	for stat in stats:
		attempt.append(stat[0])
		success.append(max(stat[1], 0.0))

	rates = np.array(success) / np.array(attempt)

	print rates

	if np.sum(rates) == 0.0:
		rates = np.ones((len(allpossible),), float) / len(allpossible)

	else:
		rates = rates / np.sum(rates)

	print rates

	return np.argmax(rates)

def realAImove(grid):

	possibleMoves = getValidMoves(grid)
	possibleMoves = np.array(removeRedundantMoves(grid, possibleMoves))

	possibleMoves2 = [(m[0], m[1]) for m in possibleMoves]


	for (i, m) in enumerate(possibleMoves2):
		if win(makeMove(deepcopy(grid), 1, m), 1):
			return m

	for m in possibleMoves2:
		if win(makeMove(deepcopy(grid), 2, m), 2):
			return m

	if (1,1) in possibleMoves2:
		return (1,1)

	diagonalMoves = [(0,0), (0,2), (2,0), (2,2)]

	mm = [mm for mm in diagonalMoves if mm in possibleMoves2]

	if len(mm) > 0:
		return mm[np.random.randint(0, len(mm))]

	return possibleMoves2 [np.random.randint(0, len(possibleMoves2))]


def impossibleState(grid):
	if np.sum(grid == 2) > np.sum(grid == 1):
		return True

	if win(grid, 1) and win(grid, 2):
		return True

#
