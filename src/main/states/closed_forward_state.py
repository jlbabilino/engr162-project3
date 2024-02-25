from robot import Robot
from robot_io import io

class ClosedForwardState:
    def __init__(self, robot: Robot, target_heading: float):
        self.robot = robot
        self.target_heading = target_heading

        self.velocity = 0.06


    def execute(self):
        error = self.robot.get_heading() - self.target_heading

        io.set_drive_left_speed(self.velocity + 0.5 * error)
        io.set_drive_right_speed(self.velocity - 0.5 * error)

        return self
