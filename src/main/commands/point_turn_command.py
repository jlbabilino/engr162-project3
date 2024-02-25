import math

from robot import Robot
from robot_io import io
from kinematics import inverse_kinematics
from util import Timer

class PointTurnCommand:
    def __init__(self, robot: Robot, target_heading: float):
        self.robot = robot
        self.target_heading = target_heading

        self.timer = Timer()

    def initialize(self):
        self.timer.start()

        self.start_heading = self.robot.get_heading()

        self.relative_angle = self.target_heading - self.start_heading
        self.omega = math.copysign(math.radians(100), self.relative_angle)
        self.turn_duration = self.relative_angle / self.omega

        self.left_speed, self.right_speed = inverse_kinematics(0, self.omega)

    def execute(self) -> bool:
        # Moving setpoint
        if (self.timer.elapsed_time() <= self.turn_duration):
            FF = self.omega
            self.set_point = self.start_heading + self.timer.elapsed_time() * self.omega
        else:
            FF = 0
            self.set_point = self.target_heading

        error = self.robot.get_heading() - self.set_point

        P = 10 * error

        control_input = FF - P

        left_speed, right_speed = inverse_kinematics(0, control_input)

        io.set_drive_left_speed(left_speed)
        io.set_drive_right_speed(right_speed)

        if self.timer.has_elapsed(self.turn_duration + 1):
            print("PointTurnCommand: Done")
            io.set_drive_left_speed(0)
            io.set_drive_right_speed(0)
            return True
        return False
