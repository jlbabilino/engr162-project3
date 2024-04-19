import math
import constants

from robot import Robot
from robot_io import io

class CalibratePosWallCommand:
    """
    Command to calibrate with a wall in front of the robot by driving forward
    or backward until the robot is centered in the cell, using the ultrasonic
    sensors
    """
    def __init__(self, robot: Robot):
        self.robot = robot

    def initialize(self):
        pass

    def execute(self) -> bool:
        d = io.front_ultrasonic_distance()

        TARGET = constants.WALL_DISTANCE / 2 - constants.FRONT_ULTRASONIC_OFFSET

        if d == math.inf:
            io.set_drive_left_speed(0)
            io.set_drive_right_speed(0)
            return True

        error = TARGET - d

        K = 0.1
        io.set_drive_left_speed(-K * error)
        io.set_drive_right_speed(-K * error)

        if abs(error) < 0.01:
            io.set_drive_left_speed(0)
            io.set_drive_right_speed(0)
            return True
        else:
            return False
