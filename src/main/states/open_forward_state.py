import math

from robot import Robot
from robot_io import io
from kinematics import inverse_kinematics
from util import Timer
from states.idle_state import IdleState
import states.open_point_turn_state

class OpenForwardState:
    def __init__(self, robot: Robot, distance: float):
        self.robot = robot
        self.distance = distance
        self.velocity = 0.06
        self.time = self.distance / self.velocity
        self.timer = Timer()
        self.timer.start()

    def execute(self):
        error = self.robot.get_heading() - self.robot.get_target_heading()
        io.set_drive_left_speed(self.velocity + 0.5 * error)
        io.set_drive_right_speed(self.velocity - 0.5 * error)
        if self.timer.has_elapsed(self.time):
            print("ForwardState: Done")
            io.set_drive_left_speed(0)
            io.set_drive_right_speed(0)

            self.robot.set_target_heading(self.robot.get_target_heading() + math.radians(-90))
            return states.open_point_turn_state.OpenPointTurnState(self.robot)
        return self
