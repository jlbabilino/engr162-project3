from dataclasses import dataclass
from enum import Enum
import math

import constants
from util import DriveWheelPositions, Pose2d
from kinematics import forward_kinematics

# class WallType(Enum):
#     FINITE_SEGMENT = 1
#     ONE_SIDED_INFINITE_RAY = 2
#     INFINITE_LINE = 3

@dataclass
class Wall:
    x1: float
    y1: float
    x2: float
    y2: float

@dataclass
class Ultrasonic:
    x_offset: float
    y_offset: float
    heading_offset: float

class Environment:
    def __init__(self, walls: list):
        self.walls = walls

    def get_walls(self) -> list[Wall]:
        return self.walls

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

# def is_wall_ultrasonic_parallel(wall: Wall, pose: Pose2d, ultrasonic_angle: float) -> float:
#     u_dx = math.cos(ultrasonic_angle)
#     u_dy = math.sin(ultrasonic_angle)

#     w_dx = wall.x2 - wall.x1
#     w_dy = wall.y2 - wall.y1

#     u_cross_w = u_dx * w_dy - u_dy * w_dx

#     return abs(u_cross_w) <= 1e-4

# def does_wall_ultrasonic_intersect(wall: Wall, pose: Pose2d, ultrasonic_angle: float) -> bool:
#     u_dx = math.cos(ultrasonic_angle)
#     u_dy = math.sin(ultrasonic_angle)

#     w_dx = wall.x2 - wall.x1
#     w_dy = wall.y2 - wall.y1

#     u_cross_w = u_dx * w_dy - u_dy * w_dx

#     if abs(u_cross_w) <= 1e-4:
#         return False

#     p_dx = pose.x - wall.x1
#     p_dy = pose.y - wall.y1

#     p_cross_w = p_dx * w_dy - p_dy * w_dx
#     p_cross_u = p_dx * u_dy - p_dy * u_dx

#     t = p_cross_w / u_cross_w
#     u = p_cross_u / u_cross_w

#     return t >= 0 and t <= 1 and u >= 0 and u <= 1