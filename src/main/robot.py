import constants
from robot_io import io
from util import CardinalDirection
from mapping.maze_map import MazeMap

class Robot:
    """
    Represents the robot's understanding of its own state, including its
    heading, and allows for running general robot code periodically.
    """

    def __init__(self):
        self.heading_offset = 0.0
        self.direction = CardinalDirection.RIGHT
        self.x_coord = 0
        self.y_coord = 0
        self.maze_map = MazeMap()

    def initialize(self):
        self.heading_offset = io.gyro_angle()
        print("Robot: initialized")

    def set_heading(self, heading: float):
        self.heading_offset = io.gyro_angle() - heading

    def get_heading(self):
        return io.gyro_angle() - self.heading_offset
    
    def set_direction(self, direction: CardinalDirection):
        self.direction = direction
        self.set_heading(direction.to_angle())

    def get_direction(self):
        return self.direction

    def periodic(self):
        pass
