class Node:
    def __init__(self, coordinate, char):
        self.coordinate = coordinate
        self.char = char
        self._neighbor = []
        self._father = None
        self.g_value = 0
        self.h_value = 0
        self.f_value = 0

    def update_f_value(self):
        self.f_value = self.g_value + self.h_value
        return self.f_value

    def add_neighbor(self, neighbor):
        self._neighbor.append(neighbor)
    
    def update_father(self, new_father):
        #print(self._father)
        #print(new_father)
        self._father = new_father

    def get_neighbors(self):
        return self._neighbor
    
    def get_father(self):
        return self._father
    
    def __str__(self):
        father = ''
        if(self._father == None):
            father = 'None'
        else:
            father = self._father
        return f"Type: {self.char}, coord: {self.coordinate}, father: {father}" 

    def __repr__(self):
        father = ''
        if(self._father == None):
            father = 'None'
        else:
            father = self._father
        return f"Type: {self.char}, coord: {self.coordinate}, father: {father}" 

def load_maze_graph(maze, start, end):
    print('loading maze graph...')
    node_maze = []
    #print(maze[0][0])
    for i in range(len(maze)):
        row = []
        for j in range(len(maze[0]) - 1):
            row.append(Node(coordinate=(i,j),char=maze[i][j].value))
        node_maze.append(row)
    #print(node_maze)
    for i in range(len(node_maze)):
        for j in range(len(node_maze[0]) - 1):
            if( (i - 1) >= 0):
                node_maze[i][j].add_neighbor(node_maze[i - 1][j])
            if((i + 1) < len(maze)):
                node_maze[i][j].add_neighbor(node_maze[i + 1][j])
            if((j - 1) >= 0):
                node_maze[i][j].add_neighbor(node_maze[i][j - 1])
            if((j + 1) < len(maze[i])):
                node_maze[i][j].add_neighbor(node_maze[i][j + 1])

        
    print('loading done!')
    return node_maze[start[0]][start[1]], node_maze[end[0]][end[1]]

    