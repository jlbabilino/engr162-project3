import math

from robot import Robot
from robot_io import io

from timer import Timer

class CalibrateHeadingWallCommand:
    """
    Command to calibrate with a wall by rotating the robot until it is parallel
    to the wall, using the ultrasonic sensors
    """
    def __init__(self, robot: Robot):
        self.robot = robot

        self.timer = Timer()

    def initialize(self):
        print("Calibrating heading")
        self.timer.start()

    def execute(self) -> bool:

        d1 = io.right_back_ultrasonic_distance()
        d2 = io.right_front_ultrasonic_distance()

        if d1 == math.inf or d2 == math.inf:
            io.set_drive_left_speed(0)
            io.set_drive_right_speed(0)
            return True

        error = d1 - d2

        # print("Error: ", error)
        if abs(error) >= 0.06:
            print("Not enough error")
            error = 0

        K = 4
        io.set_drive_left_speed(-K * error)
        io.set_drive_right_speed(K * error)

        if self.timer.has_elapsed(1.5):
            io.set_drive_left_speed(0)
            io.set_drive_right_speed(0)
            self.robot.set_heading(self.robot.get_heading_int_angle().to_angle())
            return True
        else:
            return False
