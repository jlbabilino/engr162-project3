import math

from robot import Robot
from robot_io import io
from kinematics import inverse_kinematics
from util import Timer

class ClosedPointTurnState:
    def __init__(self, robot: Robot, target_heading: float, next_state):
        self.robot = robot
        self.target_heading = target_heading
        self.next_state = next_state

        self.time = 1
        self.timer = Timer()
        self.timer.start()

        self.previous_error = 0
        self.previous_t = io.time()

        self.accum = 0

    def execute(self):
        error = self.robot.get_heading() - self.target_heading
        dt = io.time() - self.previous_t
        self.accum += error * dt

        P = 10 * error
        I = 0.0 * self.accum
        D = 0.0 * (error - self.previous_error) / dt

        control_input = P + I + D

        left_speed, right_speed = inverse_kinematics(0, -control_input)

        io.set_drive_left_speed(left_speed)
        io.set_drive_right_speed(right_speed)

        self.previous_error = error

        if self.timer.has_elapsed(self.time):
            print(f"Error: {error}")
            print("ClosedPointTurnState: Done")
            io.set_drive_left_speed(0)
            io.set_drive_right_speed(0)
            return self.next_state
        return self
