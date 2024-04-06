from robot import Robot
from robot_io import io

class IdleState:
    """
    In this state, robot does nothing. Useful for debugging, testing, etc.
    """
    def __init__(self, robot: Robot):
        self.robot = robot

    def execute(self):
        # io.print_telemetry()
        # io.magnetic_obstacle_detected()
        return self