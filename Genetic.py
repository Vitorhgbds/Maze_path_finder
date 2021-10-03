from random import randint

class Genetic:

    def __init__(self, maze, geneticConfigurations={"generationSize": 100, "initalTemp": 600}) -> None:
        self.maze = maze
        self.geneSize = self._findAllAvailablePathOnMaze()
        self.generationsSize = geneticConfigurations.generationSize
        self.initalTemp = geneticConfigurations.initalTemp
        self.currentTemp = self.initalTemp
        self.currentGeneration = []


    def _findAllAvailablePathOnMaze(self) -> int:
        spots = 0
        for row in self.maze:
            for element in self.maze[row]:
                if element.type == 'PATH':
                    spots = spots + 1
        return spots

    def _calculateHeuristc(movements) -> int:
        return 0

    def _initalizeFirstGeneration(self):
        for _ in range(self.generationsSize):
            gene = [] 
            for _ in range(self.geneSize):
                gene.append(randint(0, 4))
            self.currentGeneration.append(gene)
    
    


class Movement:
    UP = 1
    LEFT = 2
    DOWN = 3
    RIGHT = 4