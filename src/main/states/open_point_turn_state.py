import math

from robot import Robot
from robot_io import io
from kinematics import inverse_kinematics
from util import Timer
from states.idle_state import IdleState
import states.closed_point_turn_state

class OpenPointTurnState:
    def __init__(self, robot: Robot):
        self.robot = robot
        self.absolute_angle = self.robot.get_target_heading()
        self.relative_angle = self.absolute_angle - robot.get_heading()
        self.omega = math.copysign(math.radians(100), self.relative_angle)
        self.time = self.relative_angle / self.omega
        self.left_speed, self.right_speed = inverse_kinematics(0, self.omega)
        self.timer = Timer()
        self.timer.start()

    def execute(self):
        io.set_drive_left_speed(self.left_speed)
        io.set_drive_right_speed(self.right_speed)
        if self.timer.has_elapsed(self.time):
            print("PointTurnState: Done")
            # io.set_drive_left_speed(0)
            # io.set_drive_right_speed(0)
            return states.closed_point_turn_state.ClosedPointTurnState(self.robot)
        return self
