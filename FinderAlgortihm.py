import math
import time
from random import randint, random

from Position import MazePositionType


class SimulateAnnealing:

    def __init__(self, maze, startingPosition, cleanLoopsAfterComplete=False, config={"interactionNumber": 500000, "initalTemp": 10000, "decreaseEnergyPercetage" : 0.7}) -> None:
        self.maze = maze
        self.geneSize = self._findAllAvailablePathOnMaze()
        self.interactionNumber = config["interactionNumber"]
        self.initalTemp = config["initalTemp"]
        self.currentTemp = self.initalTemp
        self.startingPosition = startingPosition
        self.firstGene = ()
        self.cleanLoopsAfterComplete = cleanLoopsAfterComplete
        self.decreaseEnergyPercetage = config["decreaseEnergyPercetage"]
        self.currentGeneration = []
        self.best = None


    def _findAllAvailablePathOnMaze(self) -> int:
        spots = 0
        for row in range(len(self.maze)):
            for element in self.maze[row]:
                if element.type == MazePositionType.PATH:
                    spots = spots + 1
        return spots

    def _calculateHeuristc(self, movements):
        heuristic = 0
        visitedPositions = [self.startingPosition] # the path coord (basicaly a set of coord that the player passed)
        wallIndexes = [] # indexes of movements leading to walls
        allMovements = [] # movements to be logged
        foundS = False # have found soulutions?
        loopedPositions = [] # indexes of movements leading to alreadyKnow coordinates
        allPositions = [] # all coords
        maze = self.maze
        currentPosition = self.startingPosition
        for idx, movement in enumerate(movements):
            nextCoordinate = self._calculateNextPosition(currentPosition, movement)
            allMovements.append(Movement.tanslateMovement(movement))
            if self._isInvalidMovement(nextCoordinate, len(maze), len(maze[0])):
                heuristic = heuristic + 5
                wallIndexes.append(idx)
                continue
            else:
                nextPosition = maze[nextCoordinate[0]][nextCoordinate[1]]

                if nextPosition.type == MazePositionType.WALL:
                    heuristic = heuristic + 5
                    wallIndexes.append(idx)
                elif nextCoordinate in visitedPositions:
                    heuristic = heuristic + 3
                    allPositions.append(nextCoordinate)
                    loopedPositions.append(idx)
                    currentPosition = nextCoordinate
                else:
                    visitedPositions.append(nextCoordinate)
                    allPositions.append(nextCoordinate)
                    currentPosition = nextCoordinate
                    if nextPosition.type == MazePositionType.EXIT:
                        if len(wallIndexes) == 0:
                            heuristic = 0
                            self.best = (visitedPositions, allPositions, heuristic, allMovements, foundS, wallIndexes, True) 
                        print(f"FOUNDED, has that many walls: {len(wallIndexes)} still to fix")
                        foundS = True
                        break
            

        return (visitedPositions, allPositions, heuristic, wallIndexes, allMovements, foundS, loopedPositions)

    def _isInvalidMovement(self, coord, mazeHeight, mazeLength) -> bool:
        (y, x) = coord
        return y < 0 or y >= mazeHeight or x < 0 or x >= mazeLength

    def _calculateNextPosition(self, currentPosition, movement) -> tuple:
        (y, x) = currentPosition
        if movement == Movement.UP:
            y = y - 1
        elif movement == Movement.RIGHT:
            x = x + 1
        elif movement == Movement.DOWN:
            y = y + 1
        else:
            x = x - 1

        return (y, x)

    def _initalizeFirstSolution(self):
        gene = [] 
        for _ in range(self.geneSize):
            gene.append(randint(1, 4))
        return gene

    def _generateNeighboorGene(self, currentGene, wallIdxs, loopedIdx):
        newGene = currentGene.copy()
        selectedMovementIdx = self._selectMovementIdx(currentGene, wallIdxs, loopedIdx)
        newMovement = randint(1, 4)
        while(newMovement == currentGene[selectedMovementIdx]):
            newMovement = randint(1, 4)
        newGene[selectedMovementIdx] = newMovement
        return newGene

    def _selectMovementIdx(self, currentGene, wallIdxs, loopedIdx):
        wallIdx = self._selectRandom(wallIdxs)
        if wallIdx != None:
            print(f"SELECT WALLIDX {wallIdx}")
            return wallIdx
        loopIdx = self._selectRandom(loopedIdx)
        if loopIdx != None:
            print(f"SELECT LOOP {loopIdx}")
            return loopIdx
        idx = currentGene[randint(0, len(currentGene) -1 )]
        return idx


    def _selectRandom(self, current):
        if len(current) != 0:
            if len(current) == 1:
                return current[0]
            else:
                return current[randint(0, len(current) -1 )]
        else: 
            return None
    
    def executeAlgoritm(self, updateDraw):
        gene = self._initalizeFirstSolution()
        draw = False
        for n in range(self.interactionNumber): 
            (currentPath, allPositions, soluctionEnergyValue, wallIdxs, allMovements, foundS, loopedPositions) = self._calculateHeuristc(gene)
            if n == 0:
                self.firstGene = (currentPath, allPositions, soluctionEnergyValue, wallIdxs, allMovements, foundS, loopedPositions)
            print(f"Loop: {n}. Current Temp: {self.currentTemp}, H: {soluctionEnergyValue}")
            if(soluctionEnergyValue <= 0):
                print("Energy is perfect")
                draw = n % 1000 == 0 or foundS
                updateDraw((currentPath, soluctionEnergyValue, allMovements, allPositions, foundS, wallIdxs, draw), False)
                break
            neighboorGene = self._generateNeighboorGene(gene, wallIdxs, loopedPositions)
            (neighboorPath, allNeighboorPositions, neighboorGeneEnergyValue, _, allMovementsNeighboor, foundSNg, _) = self._calculateHeuristc(neighboorGene)
            energyValue = neighboorGeneEnergyValue - soluctionEnergyValue
            print(f"Energy: {energyValue}: neighboor: {neighboorGeneEnergyValue} - current: {soluctionEnergyValue}")
            if energyValue <= 0:
                print("neighboor is better")
                gene = neighboorGene
                draw = n % 1000 == 0 or foundS
                updateDraw((neighboorPath, neighboorGeneEnergyValue, allMovementsNeighboor, allNeighboorPositions, foundSNg, wallIdxs, draw), True)
            else:
                # 

                if foundS:
                    self.lastSolution = (currentPath, soluctionEnergyValue, allMovements, allPositions, foundS, wallIdxs, True)
                    randomProbability = 0.001
                else:    
                    randomProbability = randint(0,60) / 100
                value = math.exp(-energyValue/(self.currentTemp*1.0))
                if value < randomProbability:
                    print("neighboor is worst, but will picked")
                    gene = neighboorGene
                    currentPath = neighboorPath
                    soluctionEnergyValue = neighboorGeneEnergyValue
                    allMovements = allMovementsNeighboor
                    allPositions = allNeighboorPositions
                    foundS = foundSNg
                draw = n % 1000 == 0 or foundS
                updateDraw((currentPath, soluctionEnergyValue, allMovements, allPositions, foundS, wallIdxs, draw), True)
            self.currentTemp = self.currentTemp * self.decreaseEnergyPercetage
        if self.best != None:
            updateDraw(self.best, False)
            print('best solution found without hitting walls')
        elif self.lastSolution:
            updateDraw(self.lastSolution, False)
            print('cant find any solution without hitting a wall')

    def getFirst(self):
        return self.firstGene

class Movement:
    UP = 1
    LEFT = 2
    DOWN = 3
    RIGHT = 4

    def tanslateMovement(movement):
        if movement == Movement.UP:
            return "↑"
        elif movement == Movement.LEFT:
            return "←"
        elif movement == Movement.DOWN:
            return "↓"
        else:
            return "→"

