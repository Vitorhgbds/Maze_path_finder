import os
import random
import sys
from time import sleep
from typing import Tuple

import pygame
from numpy.random import random_integers
from pygame import key
from pygame.constants import K_ESCAPE, KEYDOWN

import config as cf
from AStar import AStar
from FinderAlgortihm import SimulateAnnealing
from Maze import Maze


class MainWindow:
    width = 1024
    height = 720
    blockSize = 10
    title = ""
    display = None
    pixelArray = None
    maze = None
    def __init__(self, title, width, height, blocksize, maze_path=''):
        self.title  = title
        self.maze = Maze(width, height, maze_path)
        self.blockSize = int(width / len(self.maze.getMaze()) * 0.85)
        self.width = self.maze.width
        self.height = self.maze.height
        self.display = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption(title)
        self.pixelArray = pygame.PixelArray(self.display)

    def _drawPixel(self, x, y, color):
        if 0<=x<self.width and 0<=y<self.height:
            self.pixelArray[x, y] = color

    def drawRectangle(self, sx, sy, width, height, color):
        pygame.draw.rect(self.display, color, pygame.Rect(sx, sy, width, height),  0, 1)
        pygame.display.flip()
        pygame.display.update()

    def drawDefaultRectagle(self, coordinate):
        (y,x) = coordinate
        self.drawRectangle(x * self.blockSize, y * self.blockSize, self.blockSize, self.blockSize,
                                         self.maze.getColor(y-1, x-1))

    def drawPlayerPath(self, coordinate, color):
        (y,x) = coordinate
        self.drawRectangle(x * self.blockSize, y * self.blockSize, self.blockSize, self.blockSize, color)

    def generateMaze(self):
        for y,x in self.maze.getToDraw():
            self.drawDefaultRectagle((y,x))
        pygame.display.update()
    
    def updatePath(self, nodes):
        print("Trying to paint")
        print(nodes)
        for node in self.maze.getToDraw():
            if node in nodes:
                self.drawPlayerPath(node)
            else:
                self.drawDefaultRectagle(node)
        self.validadeEvents()
        pygame.display.update()
        print("going on a sleep")
        sleep(2)

    def validadeEvents(self):
        mainClock = pygame.time.Clock()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if(event.key == K_ESCAPE):
                    pygame.quit()
                    sys.exit()
        mainClock.tick(60)

    lastWasFound = False

    def astar_printPath(self, pathUntilNow):
        (endPath, closeSet, openSet) = pathUntilNow
        if(len(openSet) > 0):
            for node in openSet:
                (y,x) = node.coordinate
                self.drawPlayerPath((y + 1, x + 1),(0,200,0))
                self.validadeEvents()
        if(len(closeSet) > 0):
            for node in openSet:
                (y,x) = node.coordinate
                self.drawPlayerPath((y + 1, x + 1),(200,0,0))
                self.validadeEvents()
        if(len(endPath) > 0):
            print(endPath)
            for coordinate in endPath:
                (y,x) = coordinate
                self.drawPlayerPath((y + 1, x + 1),(0,0,255))
                sleep(0.1)
                self.validadeEvents()

    def printPath(self, pathUntilNow, clean):
        (currentPath, heuristc, Allmovements, allPositions, foundSolution, still_to_Fix, draw) = pathUntilNow
        print(f"H: {heuristc}, Path {currentPath}")
        print(f"AllPositions: {allPositions}")
        print(f"AllMoviments: {Allmovements}")
        print(f"\n\n")
        #self.validadeEvents()
        if(draw):
            self.generateMaze()
            color = (random.randint(55,255),random.randint(55,255),random.randint(55,255))
            for coordinate in currentPath:
                self.validadeEvents()
                (y,x) = coordinate
                self.drawPlayerPath((y + 1, x + 1),color)
                self.validadeEvents()
        if foundSolution:
            self.generateMaze()
            sleep(1)
            color = (random.randint(55,255),random.randint(55,255),random.randint(55,255))
            if(len(still_to_Fix) > 0):
                color = (255,0,255)
            for coordinate in allPositions:
                self.validadeEvents()
                (y,x) = coordinate
                self.drawPlayerPath((y + 1, x + 1),color)
                sleep(0.01)
                self.validadeEvents()
            
        if clean: 
            print(chr(27)+'[2j')
            print('\033c')
            print('\x1bc')
            

"""
    to change configuration, change config.py
"""
if __name__=='__main__':

    os.environ['SDL_VIDEO_CENTERED'] = '1'

    pygame.init()
    window = MainWindow(cf.WINDOW_TITLE, cf.MAZE_WIDTH, cf.MAZE_HEIGHT, cf.BLOCK_SIZE, cf.MAZE_NAME)    
    window.generateMaze()
    
    astar = AStar(maze=window.maze.internalMaze,start=window.maze.startingPosition,end=window.maze.endPosition)
    astar.solve(window.astar_printPath)

    sleep(5)

    config = {"interactionNumber": 90000, "initalTemp": 500000, "decreaseEnergyPercetage" : 0.7}
    finder = SimulateAnnealing(window.maze.internalMaze, window.maze.startingPosition, False, config)
    finder.executeAlgoritm(window.printPath)

    (currentPath, allPositions, soluctionEnergyValue, wallIdxs, allMovements, foundS, loopedPositions) = finder.getFirst()
    print("firstGene")
    print(f"AllMovs {allMovements}")
    print(f"H. {soluctionEnergyValue}")

    mainClock = pygame.time.Clock()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if(event.key == K_ESCAPE):
                    pygame.quit()
                    sys.exit()
        mainClock.tick(60)

    """
    ga = GA(cf.GENERATIONS, cf.POPULATION_SIZE, cf.MUTATION_RATE, cf.START_COORDS, cf.END_COORDS, window.maze)

    run = True

    while run and ga.curgen<ga.gen and not ga.victory:
        pygame.time.Clock()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
        print("Current generation:" ,ga.curgen)
        ga.nextGen()
        toReset = set()
        for p in ga.population:
            for y,x in p.path:
                toReset.add((y,x))
                window.drawRectangle(x*window.blockSize, y*window.blockSize, window.blockSize, window.blockSize, p.color)
        for y,x in toReset:
            window.drawRectangle(x * window.blockSize, y * window.blockSize, window.blockSize, window.blockSize,
                                 (255,255,255))
        pygame.time.delay(500)
        pygame.display.update()
   
    print("Best path found", ga.bestPlayer)
    run = True
    while run:
        pygame.time.Clock()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
        for y,x in ga.bestPlayer.path:
            pygame.time.Clock().tick(30)
            window.drawRectangle(x * window.blockSize, y * window.blockSize, window.blockSize, window.blockSize,
                                 p.color)
     """

    #pygame.quit()
