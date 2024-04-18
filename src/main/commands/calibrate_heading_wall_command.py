from typing import Callable

class CalibrateHeadingWallCommand:
    """
    Command to calibrate with a wall by rotating the robot until it is parallel
    to the wall, using the ultrasonic sensors
    """
    def __init__(self, robot):
        self.robot = robot

    def initialize(self):
        pass

    def execute(self) -> bool:
        return True
