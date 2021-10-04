import os
import sys
from time import sleep

import pygame
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

    def drawPlayerPath(self, coordinate):
        (y,x) = coordinate
        self.drawRectangle(x * self.blockSize, y * self.blockSize, self.blockSize, self.blockSize, (0,0,255))

    def generateMaze(self):
        for y,x in self.maze.getToDraw():
            self.drawDefaultRectagle((y,x))
        pygame.display.update()
    
    def updatePath(self, nodes):
        print("Trying to paint")
        for node in self.maze.getToDraw():
            if node in nodes:
                self.drawPlayerPath(node)
            else:
                self.drawDefaultRectagle(node)
        pygame.display.update()
        print("going on a sleep")
        
            

"""
    to change configuration, change config.py
"""
if __name__=='__main__':

    os.environ['SDL_VIDEO_CENTERED'] = '1'

    pygame.init()
    window = MainWindow(cf.WINDOW_TITLE, cf.MAZE_WIDTH, cf.MAZE_HEIGHT, cf.BLOCK_SIZE, cf.MAZE_NAME)    
    window.generateMaze()
    astar = AStar(maze=window.maze.internalMaze,start=window.maze.startingPosition,end=window.maze.endPosition)
    astar.solve()
    #finder = SimulateAnnealing(window.maze.internalMaze, window.maze.startingPosition)
    #finder.executeAlgoritm(window.updatePath)
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
