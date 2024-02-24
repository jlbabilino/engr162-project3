import math

from robot import Robot
from robot_io import io
from kinematics import inverse_kinematics
from util import Timer
from states.idle_state import IdleState

class PointTurnState:
    def __init__(self, robot: Robot):
        self.robot = robot
        self.angle = math.radians(74)
        self.omega = math.radians(30)
        self.time = self.angle / self.omega
        self.left_speed, self.right_speed = inverse_kinematics(0, self.omega)
        self.timer = Timer()
        self.timer.start()

    def execute(self):
        io.set_drive_left_speed(self.left_speed)
        io.set_drive_right_speed(self.right_speed)
        if self.timer.has_elapsed(self.time):
            print("PointTurnState: Done")
            io.set_drive_left_speed(0)
            io.set_drive_right_speed(0)
            return IdleState(self.robot)
        return self
