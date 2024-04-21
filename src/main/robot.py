import constants
from util import IntAngle, MazeCoords, CardinalDirection
from robot_io import io
from typing import List
from mapping.maze_map import MazeMap

class Robot:
    """
    Represents the robot's understanding of its own state, including its
    heading, and allows for running general robot code periodically.
    """

    def __init__(self):
        self.heading_offset = 0.0
        self.heading_int_angle = IntAngle(0)
        self.coords = MazeCoords(0, 0)
        self.path: List[CardinalDirection] = []
        self.maze_map = MazeMap()

    def initialize(self):
        self.heading_offset = io.gyro_angle()
        print("Robot: initialized")

    def set_heading(self, heading: float):
        self.heading_offset = io.gyro_angle() - heading

    def get_heading(self):
        return io.gyro_angle() - self.heading_offset
    
    def set_heading_int_angle(self, int_angle: IntAngle):
        self.heading_int_angle = int_angle

    def get_heading_int_angle(self) -> IntAngle:
        return self.heading_int_angle

    def get_direction(self):
        return self.heading_int_angle.to_cardinal_direction()
    
    def set_maze_coords(self, coords: MazeCoords):
        self.coords = coords
    
    def get_maze_coords(self) -> MazeCoords:
        return self.coords
    
    def move_maze_coords(self, direction: CardinalDirection) -> None:
        self.coords = self.coords.move(direction)

    def periodic(self):
        pass
