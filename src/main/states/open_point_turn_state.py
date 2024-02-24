import math

from robot import Robot
from robot_io import io
from kinematics import inverse_kinematics
from util import Timer
from states.idle_state import IdleState
import states.closed_point_turn_state

class OpenPointTurnState:
    def __init__(self, robot: Robot, target_heading: float, next_state):
        self.robot = robot
        self.target_heading = target_heading
        self.next_state = next_state

        self.relative_angle = self.target_heading - robot.get_heading()
        self.omega = math.copysign(math.radians(100), self.relative_angle)
        self.time = self.relative_angle / self.omega
        self.left_speed, self.right_speed = inverse_kinematics(0, self.omega)
        self.timer = Timer()
        self.timer.start()

    def execute(self):
        io.set_drive_left_speed(self.left_speed)
        io.set_drive_right_speed(self.right_speed)
        if self.timer.has_elapsed(self.time):
            print("OpenPointTurnState: Done")
            return states.closed_point_turn_state.ClosedPointTurnState(self.robot, self.target_heading, self.next_state)
        return self
