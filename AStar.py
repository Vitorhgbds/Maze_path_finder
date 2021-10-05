import bisect
from os import close
from typing import Dict

from pygame import key
from pygame.version import ver

from Maze import Maze
from utils import Node, load_maze_graph


class AStar:
    openList = []
    closedList = set()

    def __init__(self, maze, start, end):
        self.maze = maze
        self.start = start
        self.end = end
        self.solved_path = []

    def _heuristic(self, actual_cell):
        coordinate = actual_cell.coordinate

        horizontal = abs(coordinate[0] - self.end[0])
        vertical = abs(coordinate[1] - self.end[1])

        return horizontal + vertical

    def _find_path(self, end):
        self.solved_path.append(end.coordinate)
        while(end.get_father() != None):
            #print(end.get_father())
            end = end.get_father()
            self.solved_path.append(end.coordinate)
        self.solved_path.reverse()
        print(self.solved_path)

    def solve(self, print_path):
        print('solving...')
        start, end = load_maze_graph(self.maze, self.start, self.end)
        #print(end)
        self.openList.append(start)
        walls = ['1']
        while(end not in self.closedList and len(self.openList) > 0):
            print_path((self.solved_path, self.closedList, self.openList))
            cell = self.openList.pop()
            self.closedList.add(cell)
            neighbors = cell.get_neighbors()
            #print(len(neighbors))
            #print('\n\n')
            for neighbor in neighbors:
                if neighbor.char not in walls and neighbor not in self.closedList:
                    # se o vizinho já estiver na lista aberta e o caminho dele pode ser encurtado
                    # a partir dessa celula atual, então...
                    if neighbor in self.openList:
                        if(cell.g_value + 1) < neighbor.g_value:
                            neighbor.update_father(cell)
                            neighbor.g_value = cell.g_value + 1
                            neighbor.update_f_value()
                            print('passou')
                    else:
                        self.openList.append(neighbor)
                        neighbor.update_father(cell)
                        neighbor.g_value = cell.g_value + 1
                        neighbor.h_value = self._heuristic(neighbor)
                        neighbor.update_f_value()
                        #print('passou')
            self.openList.sort(key=lambda x: x.f_value, reverse=True)
        if end in self.closedList:
            print('encontrou uma solucao')
            #print(self.closedList)
            self._find_path(end)
            print_path((self.solved_path, self.closedList, self.openList))

