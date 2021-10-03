class Position:

    def __init__(self, value):
        self.value = value
        if value == '1':
            self.type = MazePositionType.WALL
        elif value == 'E':
            self.type = MazePositionType.ENTER
        elif value == 'S':
            self.type = MazePositionType.EXIT
        else:
            self.type = MazePositionType.PATH

    def __str__(self) -> str:
        return f"Type: {type}" 

class MazePositionType:
    WALL = 1
    PATH = 0
    
    ENTER = 2
    EXIT = 3