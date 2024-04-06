"""
Useful functions and tools for simulating the robot in a 2D environment
"""

from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
import math

import constants
from util import DriveWheelPositions, Pose2d
from kinematics import forward_kinematics

@dataclass
class Wall:
    """
    Represents a wall in the 2D maze environment
    """
    x1: float
    y1: float
    x2: float
    y2: float

    def scale(self, factor: float) -> Wall:
        return Wall(self.x1 * factor, 
                    self.y1 * factor,
                    self.x2 * factor,
                    self.y2 * factor)

@dataclass
class Ultrasonic:
    """
    Represents an ultrasonic sensor on the robot
    """
    x_offset: float
    y_offset: float
    heading_offset: float

front_ultrasonic = Ultrasonic(constants.FRONT_ULTRASONIC_OFFSET, 0, 0)
left_front_ultrasonic = Ultrasonic(constants.LEFT_FRONT_ULTRASONIC_OFFSET,
                                   constants.SIDE_ULTRASONIC_OFFSET,
                                   math.radians(90))
left_back_ultrasonic = Ultrasonic(constants.LEFT_BACK_ULTRASONIC_OFFSET,
                                  constants.SIDE_ULTRASONIC_OFFSET,
                                  math.radians(90))

class Environment:
    """
    Represents the environment the robot is in, with walls and obstacles
    """
    def __init__(self, walls: list):
        self.walls = walls

    def get_walls(self) -> list[Wall]:
        return self.walls

    def scale(self, factor: float) -> Environment:
        return Environment([wall.scale(factor) for wall in self.walls])

class SimRobotState:
    """
    Represents the state of the robot in the simulation, including its
    pose, wheel velocities, wheel positions, ultrasonic sensor readings, and
    time.
    """
    def __init__(self):
        self.pose = Pose2d(0.2, 0.2, 0)

        self.left_wheel_velocity = 0
        self.right_wheel_velocity = 0

        self.left_wheel_position = 0
        self.right_wheel_position = 0

        self.front_ultrasonic_distance = +math.inf
        self.left_front_ultrasonic_distance = +math.inf
        self.left_back_ultrasonic_distance = +math.inf

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

        # self.front_ultrasonic_distance = ultrasonic_distance(self.pose, front_ultrasonic, sim_environment)
        # self.left_front_ultrasonic_distance = ultrasonic_distance(self.pose, left_front_ultrasonic, sim_environment)
        # self.left_back_ultrasonic_distance = ultrasonic_distance(self.pose, left_back_ultrasonic, sim_environment)

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
    
def ultrasonic_distance(pose: Pose2d, ultrasonic: Ultrasonic, environment: Environment) -> float:
    """
    Returns the distance from the ultrasonic sensor to the closest wall in the
    environment.
    """
    min_distance = float('inf')

    # https://www.desmos.com/calculator/qxbd0xj5ar
    for wall in environment.get_walls():
        # if is_wall_ultrasonic_parallel(wall, pose, ultrasonic.heading_offset):
        #     continue

        # if not does_wall_ultrasonic_intersect(wall, pose, ultrasonic.heading_offset):
        #     continue

        w_1x = wall.x1
        w_1y = wall.y1

        w_2x = wall.x2
        w_2y = wall.y2


        u_theta = pose.heading + ultrasonic.heading_offset

        u_dx = math.cos(u_theta)
        u_dy = math.sin(u_theta)



        p_dx = pose.x - wall.x1
        p_dy = pose.y - wall.y1

        # w_dx = wall.x2 - wall.x1
        # w_dy = wall.y2 - wall.y1

        # w_cross_p = w_dx * p_dy - w_dy * p_dx
        # w_cross_u = w_dx * ultrasonic.y_offset - w_dy * ultrasonic.x_offset

        # t = w_cross_p / w_cross_u

        # if t < 0:
        #     continue

        # u_dx = math.cos(ultrasonic.heading_offset)
        # u_dy = math.sin(ultrasonic.heading_offset)

        # u_cross_p = u_dx * p_dy - u_dy * p_dx
        # u_cross_w = u_dx * w_dy - u_dy * w_dx

        # u = u_cross_p / u_cross_w

        # if u < 0 or u > 1:
        #     continue

        # distance = abs(t)

        distance = float('inf')

        min_distance = min(min_distance, distance)

    return min_distance

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