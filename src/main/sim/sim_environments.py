
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
    
@dataclass
class Obstacle:
    """
    Represents an obstacle in the 2D maze environment
    """
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def scale(self, factor: float) -> Obstacle:
        return Obstacle(self.x * factor, self.y * factor)

class Environment:
    """
    Represents the environment the robot is in, with walls and obstacles
    """
    def __init__(self, walls: list[Wall], ir_obstacles: list[Obstacle], mag_obstacles: list[Obstacle]):
        self.walls = walls
        self.ir_obstacles = ir_obstacles
        self.mag_obstacles = mag_obstacles

    def get_walls(self) -> list[Wall]:
        return self.walls
    
    def get_ir_obstacles(self) -> list[Obstacle]:
        return self.ir_obstacles
    
    def get_mag_obstacles(self) -> list[Obstacle]:
        return self.mag_obstacles

    def scale(self, factor: float) -> Environment:
        return Environment([wall.scale(factor) for wall in self.walls],
                           [obstacle.scale(factor) for obstacle in self.ir_obstacles],
                           [obstacle.scale(factor) for obstacle in self.mag_obstacles])

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
], [Obstacle(1.5, -0.5)], [Obstacle(4.5, -2.5)]).scale(WALL_LENGTH)

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
    ], [], []).scale(WALL_LENGTH)

OFFICE_HOURS_MAZE1 = Environment([
    Wall(0,0,1,0),
    Wall(1,0,1,1),
    Wall(1,1,3,1),
    Wall(3,1,3,0),
    Wall(3,0,2,0),
    Wall(2,0,2,-3),
    Wall(2,-3,3,-3),
    Wall(3,-3,3,-4),
    Wall(3,-4,0,-4),
    Wall(0,-3,1,-3),
    Wall(1,-1,1,-3),
    Wall(0,-1,1,-1)
], [], []).scale(WALL_LENGTH)

DIFFICULT_ENVIRONEMENT_2 = Environment([
    Wall(0,0,0,2),
    Wall(0,2,5,2),
    Wall(5,2,5,1),
    Wall(5,1,8,1),
    Wall(8,1,8,2),
    Wall(9,2,9,-9),
    Wall(0,-9,9,-9),
    Wall(0,-1,1,-1),
    Wall(0,0,2,0),
    Wall(2,0,2,-1),
    Wall(3,0,3,1),
    Wall(3,1,4,1),
    Wall(4,1,4,0),
    Wall(4,0,3,0),
    Wall(1,-1,1,-2),
    Wall(0,-2,1,-2),
    Wall(0,-4,2,-4),
    Wall(2,-2,2,-4),
    Wall(4,-1,8,-1),
    Wall(5,-1,5,-2),
    Wall(3,-3,6,-3),
    Wall(4,-2,4,-3),
    Wall(3,-4,6,-4),
    Wall(3,-4,3,-6),
    Wall(0,-8,1,-8),
    Wall(1,-8,1,-7),
    Wall(1,-7,5,-7),
    Wall(3,-7,3,-8),
    Wall(5,-7,5,-5),
    Wall(5,-5,6,-5),
    Wall(6,-5,6,-4),
    Wall(7,-2,7,-5),
    Wall(7,-5,8,-5),
    Wall(8,-5,8,-4),
    Wall(8,-4,9,-4),
    Wall(5,-9,5,-8),
    Wall(5,-8,7,-8),
    Wall(7,-6,7,-8),
    Wall(7,-6,8,-6),
    Wall(8,-6,8,-7),
    Wall(8,-7,9,-7),
    Wall(0,-1,0,-9)
],[
    Obstacle(1.5, -0.5)
], []).scale(WALL_LENGTH)


"""
Environment to be used in the simulation.
"""
SIM_ENVIRONMENT = OLD_MAZE_ENVIRONMENT
