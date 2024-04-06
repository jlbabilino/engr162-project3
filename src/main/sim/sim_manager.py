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

front_ultrasonic = Ultrasonic(constants.FRONT_ULTRASONIC_OFFSET, 0, 0)
left_front_ultrasonic = Ultrasonic(constants.LEFT_FRONT_ULTRASONIC_OFFSET,
                                   constants.SIDE_ULTRASONIC_OFFSET,
                                   math.radians(90))
left_back_ultrasonic = Ultrasonic(constants.LEFT_BACK_ULTRASONIC_OFFSET,
                                  constants.SIDE_ULTRASONIC_OFFSET,
                                  math.radians(90))

class Environment:
    def __init__(self, walls: list):
        self.walls = walls

    def get_walls(self) -> list[Wall]:
        return self.walls
    
sim_environment = Environment([
    Wall(0.2, 0.2, -0.2, 0.2),
    Wall(-0.2, 0.2, -0.2, -0.2),
    Wall(-0.2, -0.2, 0.2, -0.2),
    Wall(0.2, -0.2, 0.6, -0.2),
    Wall(0.6, -0.2, 0.6, 0.2),
    Wall(0.6, 0.2, 0.6, 0.6),
    Wall(0.6, 0.6, 0.2, 0.6),
    Wall(0.2, 0.6, -0.2, 0.6),
    Wall(-0.2, 0.6, -0.6, 0.6),
    Wall(-0.6, 0.6, -0.6, 0.2),
    Wall(-0.6, 0.2, -0.6, -0.2),
])

sim_environment2 = Environment([
    Wall(0 , 0 , 2 , 0),
    Wall(2 , 0 , 2 , -1),
    Wall(2 , -1 , 4 , -1),
    Wall(4 , -1 , 4 , 0),
    Wall(4 , 0 , 7 , 0),
    Wall(7 , 0, 7, -1),
    Wall(7 , -1 , 8 -1),
    Wall(8 , -1 , 8 , -4),
    Wall(8 , -4, 9 , -4),
    Wall(9 , -4, 9 , -5),
    Wall(8, -5 , 9 , -5),
    Wall(8, -5 , 8 , -6),
    Wall(8 , -6, 11 , -6),
    Wall(0 , -1, 0 , -3),
    Wall(0 , -3, 1 , -3),
    Wall(1 , -3, 1 , -7),
    Wall(1, -7, 4 , -7),
    Wall(4, -6, 4 , -7),
    Wall(4, -6, 7, -6),
    Wall(7, -6, 7 , -7),
    Wall(7, -7, 11, -7),
    Wall(2 , -3, 3, -3),
    Wall(3, -3, 3, -2),
    Wall(3, -2, 4, -2),
    Wall(4, -2, 4, -3),
    Wall(4, -3, 7, -3),
    Wall(7, -3, 7, -5),
    Wall(4, -5, 7, -5),
    Wall(4, -4, 4, -5),
    Wall(2, -4, 4, -4),
    Wall(2, -3, 2, -4),
    Wall(1, -1, 2, -1),
    Wall(2, -1, 2, -2),
    Wall(2, -2, 1, -2),
    Wall(1, -2, 1, -1),
    Wall(5, -1, 6, -1),
    Wall(6, -1, 6, -2),
    Wall(6, -2, 5, -2),
    Wall(5, -2, 5, -1),
    Wall(2, -5, 3, -5),
    Wall(3, -5, 3, -6),
    Wall(3, -6, 2, -6),
    Wall(2, -6, 2, -5)
])

class SimRobotState:
    def __init__(self):
        self.pose = Pose2d(0, 0, 0)

        self.left_wheel_velocity = 0
        self.right_wheel_velocity = 0

        self.left_wheel_position = 0
        self.right_wheel_position = 0

        self.front_ultrasonic_distance = 255
        self.left_front_ultrasonic_distance = 255
        self.left_back_ultrasonic_distance = 255

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