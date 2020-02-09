import numpy as np
from libs import *
from copy import deepcopy


np.random.seed(1991)

grid = np.array([[0 for i in range (3)] for j in range(3)])

cross = 1
circle = 2

nStates = 3 ** 9

numberVisits = np.zeros((nStates,), int)
totalReturn = np.zeros((nStates,))
impossible = np.zeros((nStates,), bool)

for i in xrange(impossible.shape[0]):
    if impossibleState(unhash(i)):
        impossible[i] = True


nGames = 500000

winReward = 0.9
tieReward = 0.5
explorationProbability = 1.0
startExploitingEpoch = 150000

quit = False

for game in xrange(nGames):
	if game % 10000 == 0:
		print game

	if game == startExploitingEpoch:
		explorationProbability = 0.1


	turn = -1
	grid = np.zeros((3,3), int)
	visitedStatesCross = []
	visitedStatesCircle = []
	while not over(grid):
		turn += 1

		#if turn % 2 == 1:
		grid = flip(grid)

		moves = getValidMoves(grid)
		moveValues = totalReturn / numberVisits
		moveValues[np.isnan(moveValues)] = 0.0

		if explorationProbability == 1.0:
			selrnd = np.random.randint(0, len(moves))
			chosenMove = moves[selrnd]
		else:

			futureStates = [hashGrid(makeMove(deepcopy(grid), 1, i)) for i in moves]

			vals = moveValues[futureStates]
			if np.sum(vals) > 0.:
				probs = vals / np.sum(vals)

				zer = np.where(vals == 0)[0]
				if len(zer > 0):
					probs *= (1 - explorationProbability)
					probs[zer] = explorationProbability / zer.shape[0]

				chosenMoveInd = np.random.choice(len(moves), 1, p=probs)[0]
				chosenMove = moves[chosenMoveInd]
			else:
				chosenMoveInd = np.random.choice(len(moves), 1)[0]
				chosenMove = moves[chosenMoveInd]


		makeMove(grid, 1, chosenMove)


		state = hashGrid(grid)
		if state == 19399:
			quit = True
			break
		numberVisits[state] += 1

		if turn % 2 == 1:
			visitedStatesCircle.append(state)
		else:
			visitedStatesCross.append(state)

		#if turn % 2 == 1:
		#	grid = flip(grid)

	if win(grid, cross):
		l = len(visitedStatesCross) - 1
		for i, s in enumerate(visitedStatesCross):
			totalReturn[s] += winReward ** (l - i)

	elif win(grid, circle):
		l = len(visitedStatesCircle) - 1
		for i, s in enumerate(visitedStatesCircle):
			totalReturn[s] += winReward ** (l - i)

	else:
		l = len(visitedStatesCross) - 1
		for i, s in enumerate(visitedStatesCross):
			totalReturn[s] += tieReward ** (l - i)

		l = len(visitedStatesCircle) - 1
		for i, s in enumerate(visitedStatesCircle):
			totalReturn[s] += tieReward ** (l - i)

	if quit:
		break


explorationProbability = 0.05
for game in xrange(nGames):
	if game % 10000 == 0:
		print game


	turn = -1
	grid = np.zeros((3,3), int)
	visitedStatesCross = []
	visitedStatesCircle = []
	while not over(grid):
		turn += 1

		#if turn % 2 == 1:
		grid = flip(grid)

		moves = getValidMoves(grid)
		moveValues = totalReturn / numberVisits
		moveValues[np.isnan(moveValues)] = 0.0

		futureStates = [hashGrid(makeMove(deepcopy(grid), 1, i)) for i in moves]

		vals = moveValues[futureStates]

		if np.random.rand() < explorationProbability:
			chosenMoveInd = np.random.randint(0, len(moves))
		else:
			chosenMoveInd = np.argmax(vals)

		chosenMove = moves[chosenMoveInd]

		makeMove(grid, 1, chosenMove)

		state = hashGrid(grid)

		numberVisits[state] += 1

		if turn % 2 == 1:
			visitedStatesCircle.append(state)
		else:
			visitedStatesCross.append(state)

		#if turn % 2 == 1:
		#	grid = flip(grid)

	if win(grid, cross):
		l = len(visitedStatesCross) - 1
		for i, s in enumerate(visitedStatesCross):
			totalReturn[s] += winReward ** (l - i)

	elif win(grid, circle):
		l = len(visitedStatesCircle) - 1
		for i, s in enumerate(visitedStatesCircle):
			totalReturn[s] += winReward ** (l - i)

	else:
		l = len(visitedStatesCross) - 1
		for i, s in enumerate(visitedStatesCross):
			totalReturn[s] += tieReward ** (l - i)

		l = len(visitedStatesCircle) - 1
		for i, s in enumerate(visitedStatesCircle):
			totalReturn[s] += tieReward ** (l - i)
