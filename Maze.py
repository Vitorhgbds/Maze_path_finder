from random import randint

from Position import *


class Maze:
    wallRGB, wayRGB, enterRGB, exitRGB = (0, 0, 0), (255, 255, 255), (255, 0, 0), (0, 255, 0)

    def __init__(self, width, height, maze_name=''):
        self.width = width
        self.height = height

        # generate an empty maze
        self.frontier = set()
        self.visited = set()
        self.toDraw = set()
        self.maze = []
        self.internalMaze = []

        self.visited.add((0, 0))
        with open(maze_name) as maze:
            lines = maze.readlines()
            for i in range(len(lines)):
                viewRow = []
                row = []
                line = lines[i]
                for j in range(len(line)):
                    if line[j] == '0' and not line[j] == '\n':
                        viewRow.append(Maze.wayRGB)
                        row.append(Position('0', i, j))
                        self.toDraw.add((i+1,j+1))
                    elif line[j] == 'E':
                        viewRow.append(Maze.enterRGB)
                        row.append(Position('E', i, j))
                        self.startingPosition = (i , j)
                        self.toDraw.add((i + 1, j + 1))
                    elif line[j] == 'S':
                        self.endPosition = (i,j)
                        viewRow.append(Maze.exitRGB)
                        row.append(Position('S', i, j))
                        self.toDraw.add((i+1,j+1))
                    else:
                        viewRow.append(Maze.wallRGB)
                        row.append(Position('1', i, j))
                        self.frontier.add((i,j))
                self.maze.append(viewRow)
                self.internalMaze.append(row)


    def _clamp(self, n, minN, maxN):
        return min(max(minN, n), maxN)

    def _addWalls(self, y, x):
        for o in Maze.offset:
            cell = (y + o[0], x + o[1])
            if self._range(cell[0], cell[1]) and cell not in self.visited and cell not in self.frontier and \
                    self.maze[cell[0]][cell[1]] == Maze.wayRGB:
                self.frontier.add(cell)

    def _findVisitedNear(self, y, x):
        return [(o[0] + y, o[1] + x) for o in Maze.offset if (o[0] + y, o[1] + x) in self.visited]

    def _range(self, y, x):
        return 0 <= x < self.width and 0 <= y < self.height

    def getMaze(self):
        return self.maze

    def getFrontier(self):
        return self.frontier

    def getToDraw(self):
        return self.toDraw

    def getColor(self, y, x):
        return self.maze[y][x]

    def workOneStep(self):
        self.toDraw.clear()
        if len(self.frontier) > 0:
            cell = self.frontier.pop()

            near = self._findVisitedNear(cell[0], cell[1])
            inmaze = near[randint(0, len(near) - 1)]

            dy, dx = self._clamp(cell[0] - inmaze[0], -1, 1), self._clamp(cell[1] - inmaze[1], -1, 1)

            if dy != 0:
                self.maze[inmaze[0] + dy][inmaze[1]] = Maze.wayRGB
                self.toDraw.add((inmaze[0] + dy, inmaze[1]))
            if dx != 0:
                self.maze[inmaze[0]][inmaze[1] + dx] = Maze.wayRGB
                self.toDraw.add((inmaze[0], inmaze[1] + dx))

            self.visited.add(cell)
            self.toDraw.add(cell)

            self._addWalls(cell[0], cell[1])

    def _quad(self, x, y, w, h, img, color):
        for dy in range(h): img[y + dy] += [color for i in range(w)]

    def _loadMaze(self, maze_name):
        lab = ""
        with open(maze_name) as maze:
            lines = maze.readlines()
            for o in self.offset:
                for i in range(len(lines)):
                    line = lines[i]
                    for j in range(len(line)):
                        cell = (i + 1 + o[0], j + 1 + o[1])
                        if self._range(cell[0], cell[1]) and not line[j] == '1':
                            self.toDraw.add(cell)

    def genImg(self, wb, hb):
        img = [[] for i in range(self.height * hb)]
        tx, ty = 0, 0

        for y in range(self.height):
            for x in range(self.width):
                self._quad(tx, ty, wb, hb, img, self.maze[y][x])
                tx += wb
            ty += hb
        return img
