from dataclasses import dataclass
from enum import Enum
import math

from util import DriveWheelPositions, Pose2d
from kinematics import forward_kinematics

class WallType(Enum):
    FINITE_SEGMENT = 1
    ONE_SIDED_INFINITE_RAY = 2
    INFINITE_LINE = 3

@dataclass
class Wall:
    x1: float
    y1: float
    x2: float
    y2: float
    wall_type: WallType
    

# class Environment:
#     def __init__(self):
#         walls = []

class SimRobotState:
    def __init__(self):
        self.pose = Pose2d(0, 0, 0)

        self.left_wheel_velocity = 0
        self.right_wheel_velocity = 0

        self.left_wheel_position = 0
        self.right_wheel_position = 0

        self.time = 0

    def update(self, time: float):
        dt = time - self.time

        prev_wheel_positions = DriveWheelPositions(self.left_wheel_position,
                                                   self.right_wheel_position)

        self.left_wheel_position += self.left_wheel_velocity * dt
        self.right_wheel_position += self.right_wheel_velocity * dt

        curr_wheel_positions = DriveWheelPositions(self.left_wheel_position,
                                                   self.right_wheel_position)

        self.pose = forward_kinematics(self.pose, prev_wheel_positions,
                                       curr_wheel_positions)

        self.time = time

    def set_left_wheel_velocity(self, velocity: float):
        self.left_wheel_velocity = velocity

    def set_right_wheel_velocity(self, velocity: float):
        self.right_wheel_velocity = velocity

    def get_left_wheel_position(self):
        return self.left_wheel_position
    
    def get_right_wheel_position(self):
        return self.right_wheel_position
    
    def get_pose(self):
        return self.pose
