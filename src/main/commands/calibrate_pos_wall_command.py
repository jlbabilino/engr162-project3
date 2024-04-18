from typing import Callable

class CalibratePosWallCommand:
    """
    Command to calibrate with a wall in front of the robot by driving forward
    or backward until the robot is centered in the cell, using the ultrasonic
    sensors
    """
    def __init__(self, robot):
        self.robot = robot

    def initialize(self):
        pass

    def execute(self) -> bool:
        return True
