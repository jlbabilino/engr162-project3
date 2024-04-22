from dataclasses import dataclass
from typing import Optional, List
from enum import Enum
from util import CardinalDirection, MazeCoords

@dataclass
class DetectedHazard:
    """
    Represents a detected hazard in the maze.
    """
    x: int
    y: int
    hazard_type: str
    parameter_of_interest: str
    parameter_value: float

class MazeMapCellType(Enum):
    VISITED = 1
    NOT_VISITED = 0
    STARTING_POINT = 5
    HEAT_SOURCE = 2
    MAGNETIC_SOURCE = 3
    EXIT_POINT = 4

@dataclass
class MazeMapCell:
    left_wall: Optional[bool] = None
    bottom_wall: Optional[bool] = None

    cell_type: MazeMapCellType = MazeMapCellType.NOT_VISITED

class MazeDecisionStatus(Enum):
    EXIT = 0
    STUCK = 1
    BACKTRACK = 2
    NO_WALL_IN_WAY = 3
    MAYBE_WALL_IN_WAY = 4

@dataclass
class MazeDecision:
    """
    Represents a decision made by the robot in the maze.
    """
    direction: CardinalDirection
    """
    The status of the decision, indicating whether or not robot is stuck, if it
    has exit the maze, whether or not it should backtrack, or whether or not it
    knows for sure that there is no wall in the way.
    """
    status: MazeDecisionStatus

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

        # self.maze_map[0][0].left_wall = True
        # self.maze_map[0][0].bottom_wall = True
        # self.maze_map[1][0].bottom_wall = True

        self.maze_path = []

        self.ir_hazards: List[DetectedHazard] = []
        self.mag_hazards: List[DetectedHazard] = []

    def optimal_next_move(self, x: int, y: int, path: List[CardinalDirection]) -> MazeDecision:
        """
        Given the current position, return the optimal next move to make. The
        boolean value indicates whether the next cell is known to be safe to
        move to, meaning it is known that there is no wall or obstacle in the
        way.
        """
        maybe_wall_in_way_dirs: List[CardinalDirection] = []
        no_wall_in_way_dirs: List[CardinalDirection] = []
        for direction in (CardinalDirection.RIGHT,
                          CardinalDirection.DOWN,
                          CardinalDirection.UP,
                          CardinalDirection.LEFT):
            if len(path) > 0 and direction == path[-1].reverse():
                continue
            coords = MazeCoords(x, y).move(direction)
            adjacent_cell_type = self.maze_map[coords.y][coords.x].cell_type
            if (adjacent_cell_type == MazeMapCellType.VISITED
                    or adjacent_cell_type == MazeMapCellType.STARTING_POINT
                    or adjacent_cell_type == MazeMapCellType.HEAT_SOURCE
                    or adjacent_cell_type == MazeMapCellType.MAGNETIC_SOURCE):
                continue
            wall = self.get_wall(x, y, direction)
            if wall == False or wall == None:
                maybe_wall_in_way_dirs.append(direction)
            if wall == False:
                no_wall_in_way_dirs.append(direction)

        if x >= 5:
            return MazeDecision(None, MazeDecisionStatus.EXIT)

        print("Safe:  ", [d.name for d in no_wall_in_way_dirs])
        print("Safe?: ", [d.name for d in maybe_wall_in_way_dirs])
        
        if len(no_wall_in_way_dirs) > 0:
            return MazeDecision(no_wall_in_way_dirs[0], MazeDecisionStatus.NO_WALL_IN_WAY)
        elif len(maybe_wall_in_way_dirs) > 0:
            return MazeDecision(maybe_wall_in_way_dirs[0], MazeDecisionStatus.MAYBE_WALL_IN_WAY)
        elif len(path) > 0:
            return MazeDecision(path[-1].reverse(), MazeDecisionStatus.BACKTRACK)
        else:
            return MazeDecision(None, MazeDecisionStatus.STUCK)

    def expand_map(self, x: int, y: int):
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

    def set_wall(self, x: int, y: int, direction: CardinalDirection, exists: bool):
        if direction == CardinalDirection.LEFT:
            self.set_left_wall(x, y, exists)
        elif direction == CardinalDirection.RIGHT:
            self.set_right_wall(x, y, exists)
        elif direction == CardinalDirection.UP:
            self.set_top_wall(x, y, exists)
        elif direction == CardinalDirection.DOWN:
            self.set_bottom_wall(x, y, exists)

        self.expand_map(x, y)

    def get_bottom_wall(self, x: int, y: int) -> Optional[bool]:
        return self.maze_map[y][x].bottom_wall
    def get_left_wall(self, x: int, y: int) -> Optional[bool]:
        return self.maze_map[y][x].left_wall
    def get_right_wall(self, x: int, y: int) -> Optional[bool]:
        return self.maze_map[y][x + 1].left_wall
    def get_top_wall(self, x: int, y: int) -> Optional[bool]:
        return self.maze_map[y + 1][x].bottom_wall
    
    def get_wall(self, x: int, y: int, direction: CardinalDirection) -> Optional[bool]:
        if direction == CardinalDirection.LEFT:
            return self.get_left_wall(x, y)
        elif direction == CardinalDirection.RIGHT:
            return self.get_right_wall(x, y)
        elif direction == CardinalDirection.UP:
            return self.get_top_wall(x, y)
        elif direction == CardinalDirection.DOWN:
            return self.get_bottom_wall(x, y)
        
    def get_wall_relative(self, x: int, y: int,
                          robot_direction: CardinalDirection,
                          wall_direction: CardinalDirection):
        direction = robot_direction.plus(wall_direction)
        return self.get_wall(x, y, direction)

    def update_visited_cell(self, x, y):
        """
        Update the cell at (x, y) with the given walls. Sets the cell as
        visited.
        """
        self.maze_map[y][x].cell_type = MazeMapCellType.VISITED

        self.expand_map(x, y)

    def update_ir_hazard(self, x: int, y: int, strength: float):
        """
        Update the cell at (x, y) with the given hazard.
        """
        self.maze_map[y][x].cell_type = MazeMapCellType.HEAT_SOURCE

        self.expand_map(x, y)

        self.ir_hazards.append(DetectedHazard(x, y, "High Temperature Heat Source", "Radiated Power (W)", strength))

    def update_mag_hazard(self, x: int, y: int, strength: float):
        """
        Update the cell at (x, y) with the given hazard.
        """
        self.maze_map[y][x].cell_type = MazeMapCellType.MAGNETIC_SOURCE

        self.expand_map(x, y)

        self.mag_hazards.append(DetectedHazard(x, y, "Electrical/Magnetic Activity Source", "Field Strength (uT)", strength))

    def update_end_cell(self, x, y):
        """
        Update the cell at (x, y) as the exit point.
        """
        self.maze_map[y][x].cell_type = MazeMapCellType.EXIT_POINT

        self.expand_map(x, y)

    def print(self):
        print("Team: 40")
        print("Map: 0")
        print("Unit Length: 40")
        print("Unit: cm")
        print(f"Origin: ({abs(self.x_min)},{abs(self.y_min)})")

        for y in range(self.y_max, self.y_min - 1, -1):
            print(",".join([str(self.maze_map[y][x].cell_type.value)
                            for x in range(self.x_min, self.x_max + 1, +1)]))
        print()
        print("Hazard Type, Parameter of Interest, Parameter Value, Hazard X Coordinate, Hazard Y Coordinate")
        for hazard in self.ir_hazards + self.mag_hazards:
            print(f"{hazard.hazard_type}, {hazard.parameter_of_interest}, {hazard.parameter_value}, {hazard.x}, {hazard.y}")
            
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

# testMaze.update_ir_hazard(1, 1, 100)

# testMaze.pretty_print()
