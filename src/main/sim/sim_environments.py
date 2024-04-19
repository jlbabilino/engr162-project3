
from __future__ import annotations
from dataclasses import dataclass
import sim.sim_util as su

WALL_LENGTH = 0.4

@dataclass
class Wall:
    """
    Represents a wall in the 2D maze environment
    """
    x1: float
    y1: float
    x2: float
    y2: float

    def scale(self, factor: float) -> Wall:
        return Wall(self.x1 * factor, 
                    self.y1 * factor,
                    self.x2 * factor,
                    self.y2 * factor)

class Environment:
    """
    Represents the environment the robot is in, with walls and obstacles
    """
    def __init__(self, walls: list):
        self.walls = walls

    def get_walls(self) -> list[Wall]:
        return self.walls

    def scale(self, factor: float) -> Environment:
        return Environment([wall.scale(factor) for wall in self.walls])

OLD_MAZE_ENVIRONMENT = Environment([
    Wall(0,  0,  2,  0),
    Wall(2,  0,  2, -1),
    Wall(2, -1,  4, -1),
    Wall(4, -1,  4,  0),
    Wall(4,  0,  7,  0),
    Wall(7,  0,  7, -1),
    Wall(7, -1,  8, -1),
    Wall(8, -1,  8, -4),
    Wall(8, -4,  9, -4),
    Wall(9, -4,  9, -5),
    Wall(8, -5,  9, -5),
    Wall(8, -5,  8, -6),
    Wall(8, -6, 11, -6),
    Wall(0, -1,  0, -3),
    Wall(0, -3,  1, -3),
    Wall(1, -3,  1, -7),
    Wall(1, -7,  4, -7),
    Wall(4, -6,  4, -7),
    Wall(4, -6,  7, -6),
    Wall(7, -6,  7, -7),
    Wall(7, -7, 11, -7),
    Wall(2, -3,  3, -3),
    Wall(3, -3,  3, -2),
    Wall(3, -2,  4, -2),
    Wall(4, -2,  4, -3),
    Wall(4, -3,  7, -3),
    Wall(7, -3,  7, -5),
    Wall(4, -5,  7, -5),
    Wall(4, -4,  4, -5),
    Wall(2, -4,  4, -4),
    Wall(2, -3,  2, -4),
    Wall(1, -1,  2, -1),
    Wall(2, -1,  2, -2),
    Wall(2, -2,  1, -2),
    Wall(1, -2,  1, -1),
    Wall(5, -1,  6, -1),
    Wall(6, -1,  6, -2),
    Wall(6, -2,  5, -2),
    Wall(5, -2,  5, -1),
    Wall(2, -5,  3, -5),
    Wall(3, -5,  3, -6),
    Wall(3, -6,  2, -6),
    Wall(2, -6,  2, -5)
]).scale(WALL_LENGTH)

DIFFICULT_ENVIRONEMENT = Environment([
    Wall(0,0,2,0),
    Wall(2,0,2,-2),
    Wall(1,-2,2,-2),
    Wall(1,-1,1,-3),
    Wall(1,-1,2,-1),
    Wall(0,-1,0,-4),
    Wall(0,-4,1,-4),
    Wall(1,-4,1,-6),
    Wall(1,-6,4,-6),
    Wall(4,-3, 4, -6),
    Wall(3,-4, 4, -4),
    Wall(2,-4,2,-5),
    Wall(2,-5,3,-5),
    Wall(3,-4,3,-5),
    Wall(1,-3,3,-3),
    Wall(3,-2,3,-3),
    Wall(2,-1,5,-1),
    Wall(5,-1,5,-2),
    Wall(5,-2,6,-2),
    Wall(6,-2,6,-3),
    Wall(6,-3,7,-3),
    Wall(4, -3, 5, -3),
    Wall(5, -3, 5, -5),
    Wall(5,-5,6,-5),
    Wall(6,-4,6,-5),
    Wall(6,-4,7,-4)
    ]).scale(WALL_LENGTH)


"""
Environment to be used in the simulation.
"""
SIM_ENVIRONMENT = DIFFICULT_ENVIRONEMENT
