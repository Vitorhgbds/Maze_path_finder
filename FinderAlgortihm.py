from random import randint, random
from Position import MazePositionType
import math

class SimulateAnnealing:

    def __init__(self, maze, startingPosition, config={"interactionNumber": 500000, "initalTemp": 10000, "decreaseEnergyPercetage" : 0.7}) -> None:
        self.maze = maze
        self.geneSize = self._findAllAvailablePathOnMaze()
        self.interactionNumber = config["interactionNumber"]
        self.initalTemp = config["initalTemp"]
        self.currentTemp = self.initalTemp
        self.startingPosition = startingPosition
        self.decreaseEnergyPercetage = config["decreaseEnergyPercetage"]
        self.currentGeneration = []


    def _findAllAvailablePathOnMaze(self) -> int:
        spots = 0
        for row in range(len(self.maze)):
            for element in self.maze[row]:
                if element.type == MazePositionType.PATH:
                    spots = spots + 1
        return spots

    def _calculateHeuristc(self, movements) -> int:
        heuristic = 10
        visitedPositions = []
        maze = self.maze
        currentPosition = self.startingPosition
        for movement in movements:
            nextCoordinate = self._calculateNextPosition(currentPosition, movement)

            if self._isInvalidMovement(nextCoordinate, len(maze), len(maze[0])):
                heuristic = heuristic + 30
                continue
            else:
                nextPosition = maze[nextCoordinate[0]][nextCoordinate[1]]

                if nextPosition.type == MazePositionType.WALL:
                    heuristic = heuristic + 1
                elif nextCoordinate in visitedPositions:
                    heuristic = heuristic + 5
                    currentPosition = nextCoordinate
                else:
                    visitedPositions.append(nextCoordinate)
                    currentPosition = nextCoordinate
                    if nextPosition.type == MazePositionType.EXIT:
                        heuristic = heuristic - 10
                        break
            

        return (visitedPositions, heuristic)

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

    def _generateNeighboorGene(self, currentGene):
        newGene = currentGene.copy()
        selectedMovementIdx = currentGene[randint(0, len(currentGene) -1 )] #Tentar de alguma forma pegar algum gene que esteja errado.
        newMovement = randint(1, 4)
        while(newMovement == currentGene[selectedMovementIdx]):
            newMovement = randint(1, 4)
        newGene[selectedMovementIdx] = newMovement
        return newGene

    
    def executeAlgoritm(self, updateDraw):
        gene = self._initalizeFirstSolution()
        for _ in range(self.interactionNumber):
            (currentPath, soluctionEnergyValue) = self._calculateHeuristc(gene)
            if(soluctionEnergyValue <= 0):
                 updateDraw(currentPath)
                 break
            neighboorGene = self._generateNeighboorGene(gene)
            (neighboorPath, neighboorGeneEnergyValue) = self._calculateHeuristc(neighboorGene)
            energyValue = neighboorGeneEnergyValue - soluctionEnergyValue

            if energyValue <= 0:
                gene = neighboorGene
                updateDraw(neighboorPath)
            else:
                randomProbability = random()
                value = math.exp(-energyValue/(self.currentTemp*1.0))
                if value < randomProbability:
                    gene = neighboorGene
                    currentPath = neighboorPath
                
                updateDraw(currentPath)
            self.currentTemp = self.currentTemp * self.decreaseEnergyPercetage


class Movement:
    UP = 1
    LEFT = 2
    DOWN = 3
    RIGHT = 4

