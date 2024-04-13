from dataclasses import dataclass
from typing import Optional
from enum import Enum

class MazeMapCellType(Enum):
    VISITED = 1
    NOT_VISITED = 0
    STARTING_POINT = 5
    HEAT_SOURCE = 2
    MAGNETIC_SOURCE = 3
    EXIT_POINT = 4

@dataclass
class MazeMapCell:
    left_wall: bool = False
    bottom_wall: bool = False

    cell_type: MazeMapCellType = MazeMapCellType.NOT_VISITED

class MazeMap:
    def __init__(self):
        self.x_min = 0
        self.x_max = 0
        self.y_min = 0
        self.y_max = 0

        self.maze_map = []
        for y in range(50):
            row = []
            for x in range(50):
                row.append(MazeMapCell())
            self.maze_map.append(row)

        self.maze_map[0][0].cell_type = MazeMapCellType.STARTING_POINT

    def set_cell_type(self, x: int, y: int, cell_type: MazeMapCellType):
        self.maze_map[y][x].cell_type = cell_type

        self.x_min = min(self.x_min, x)
        self.x_max = max(self.x_max, x)
        self.y_min = min(self.y_min, y)
        self.y_max = max(self.y_max, y)

    def set_bottom_wall(self, x: int, y: int, exists: bool):
        self.maze_map[y][x].bottom_wall = exists
    def set_left_wall(self, x: int, y: int, exists: bool):
        self.maze_map[y][x].left_wall = exists
    def set_right_wall(self, x: int, y: int, exists: bool):
        self.maze_map[y][x + 1].left_wall = exists
    def set_top_wall(self, x: int, y: int, exists: bool):
        self.maze_map[y + 1][x].bottom_wall = exists

    def get_bottom_wall(self, x: int, y: int):
        return self.maze_map[y][x].bottom_wall
    def get_left_wall(self, x: int, y: int):
        return self.maze_map[y][x].left_wall
    def get_right_wall(self, x: int, y: int):
        return self.maze_map[y][x + 1].left_wall
    def get_top_wall(self, x: int, y: int):
        return self.maze_map[y + 1][x].bottom_wall

    def update_visited_cell(self, x, y,
                            left_wall: Optional[bool] = None,
                            bottom_wall: Optional[bool] = None,
                            right_wall: Optional[bool] = None,
                            top_wall: Optional[bool] = None):
        """
        Update the cell at (x, y) with the given walls. Sets the cell as
        visited.
        """
        self.set_cell_type(x, y, MazeMapCellType.VISITED)

        if left_wall is not None:
            self.set_left_wall(x, y, left_wall)
        if bottom_wall is not None:
            self.set_bottom_wall(x, y, bottom_wall)
        if right_wall is not None:
            self.set_right_wall(x, y, right_wall)
        if top_wall is not None:
            self.set_top_wall(x, y, top_wall)

    def print(self):
        print("Team: 40")
        print("Map: 0")
        print("Unit Length: 40")
        print("Unit: cm")
        print(f"Origin: ({abs(self.x_min)},{abs(self.y_min)})")

        for y in range(self.y_max, self.y_min - 1, -1):
            print(",".join([str(self.maze_map[y][x].cell_type.value)
                            for x in range(self.x_min, self.x_max + 1, +1)]))
            
    def pretty_print(self):
        """
        Print the maze beautifully using Unicode characters to represent walls.
        Most of this code is AI-generated lmao.
        """
        print(f"Origin: ({abs(self.x_min)},{abs(self.y_min)})")

        print(" ", end="")
        for x in range(self.x_min - 1, self.x_max + 2, +1):
            cell = self.maze_map[self.y_max + 1][x]
            if cell.bottom_wall:
                print(" ───", end="")
            else:
                print("    ", end="")
        print()
        for y in range(self.y_max, self.y_min - 1, -1):
            for x in range(self.x_min - 1, self.x_max + 2, +1):
                cell = self.maze_map[y][x]
                if cell.left_wall:
                    print(" │ ", end="")
                else:
                    print("   ", end="")
                if cell.cell_type == MazeMapCellType.VISITED:
                    print("X", end="")
                elif cell.cell_type == MazeMapCellType.NOT_VISITED:
                    print("⚬", end="")
                elif cell.cell_type == MazeMapCellType.STARTING_POINT:
                    print("S", end="")
                elif cell.cell_type == MazeMapCellType.HEAT_SOURCE:
                    print("H", end="")
                elif cell.cell_type == MazeMapCellType.MAGNETIC_SOURCE:
                    print("M", end="")
                elif cell.cell_type == MazeMapCellType.EXIT_POINT:
                    print("E", end="")
            print()
            print(" ", end="")
            for x in range(self.x_min - 1, self.x_max + 2, +1):
                cell = self.maze_map[y][x]
                if cell.bottom_wall:
                    print(" ───", end="")
                else:
                    print("    ", end="")
            print()

# testMaze = MazeMap()

# testMaze.update_visited_cell(0, 0, True, True, True, True)
# testMaze.update_visited_cell(1, 0, False, True, True, True)
# testMaze.update_visited_cell(0, 1, False, True, True, True)
# testMaze.update_visited_cell(0, 2, True, True, True, True)
# testMaze.update_visited_cell(-3, 0, True, True, True, True)
# testMaze.update_visited_cell(0, -4, True, True, True, True)

# testMaze.pretty_print()
