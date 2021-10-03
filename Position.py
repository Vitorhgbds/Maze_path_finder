class Position:

    def __init__(self, value, y, x):
        self.value = value
        self.point = (y,x)
        if value == '1':
            self.type = MazePositionType.WALL
        elif value == 'E':
            self.type = MazePositionType.ENTER
        elif value == 'S':
            self.type = MazePositionType.EXIT
        else:
            self.type = MazePositionType.PATH

    def __str__(self) -> str:
        return f"Type: {self._getPosName()}, coord: {self.point}" 

    def __repr__(self) -> str:
        return f"Type: {self._getPosName()}, coord: {self.point}" 

    def _getPosName(self):
        if self.type == MazePositionType.WALL:
            return "WALL"
        elif self.type == MazePositionType.PATH:
            return 'PATH'
        elif self.type == MazePositionType.EXIT:
            return 'EXIT'
        else:
            return 'ENTER'
    
class MazePositionType:
    WALL = 0
    PATH = 1
    
    ENTER = 2
    EXIT = 3
