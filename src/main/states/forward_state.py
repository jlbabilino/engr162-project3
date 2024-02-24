from robot import Robot
from robot_io import io
from kinematics import inverse_kinematics
from util import Timer
from states.idle_state import IdleState

class ForwardState:
    def __init__(self, robot: Robot):
        self.robot = robot
        self.distance = 0.4
        self.velocity = 0.06
        self.time = self.distance / self.velocity
        self.timer = Timer()
        self.timer.start()

    def execute(self):
        io.set_drive_left_speed(self.velocity)
        io.set_drive_right_speed(self.velocity)
        if self.timer.has_elapsed(self.time):
            print("ForwardState: Done")
            io.set_drive_left_speed(0)
            io.set_drive_right_speed(0)
            return IdleState(self.robot)
        return self
