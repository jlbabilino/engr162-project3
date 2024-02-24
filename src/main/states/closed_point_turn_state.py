import math

from robot import Robot
from robot_io import io
from kinematics import inverse_kinematics
from util import Timer
from states.idle_state import IdleState
import states.open_forward_state

class ClosedPointTurnState:
    def __init__(self, robot: Robot):
        self.robot = robot
        self.absolute_angle = self.robot.get_target_heading()

        self.time = 1
        self.timer = Timer()
        self.timer.start()

        self.previous_error = 0
        self.previous_t = io.time()

        self.accum = 0

    def execute(self):
        error = self.robot.get_target_heading() - self.absolute_angle
        dt = io.time() - self.previous_t
        self.accum += error * dt

        print(f"Error: {error}")

        P = 10 * error
        I = 0.0 * self.accum
        D = 0.0 * (error - self.previous_error) / dt

        control_input = P + I + D

        left_speed, right_speed = inverse_kinematics(0, -control_input)

        io.set_drive_left_speed(left_speed)
        io.set_drive_right_speed(right_speed)

        self.previous_error = error

        if self.timer.has_elapsed(self.time):
            print("ClosedPointTurnState: Done")
            io.set_drive_left_speed(0)
            io.set_drive_right_speed(0)
            return states.open_forward_state.OpenForwardState(self.robot, 0.2)
            # return IdleState(self.robot)
        return self
