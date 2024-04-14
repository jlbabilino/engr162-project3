"""
Useful functions and tools for simulating the robot in a 2D environment
"""

from dataclasses import dataclass
from enum import Enum
import math

import constants
from util import DriveWheelPositions, Pose2d, Transform2d, Translation2d
import sim.sim_environments as envs
from kinematics import forward_kinematics

@dataclass
class Ultrasonic:
    """
    Represents an ultrasonic sensor on the robot
    """
    x_offset: float
    y_offset: float
    heading_offset: float

FRONT_ULTRASONIC = Ultrasonic(constants.FRONT_ULTRASONIC_OFFSET, 0, 0)
LEFT_FRONT_ULTRASONIC = Ultrasonic(constants.LEFT_FRONT_ULTRASONIC_OFFSET,
                                   constants.SIDE_ULTRASONIC_OFFSET,
                                   math.radians(90))
LEFT_BACK_ULTRASONIC = Ultrasonic(constants.LEFT_BACK_ULTRASONIC_OFFSET,
                                  constants.SIDE_ULTRASONIC_OFFSET,
                                  math.radians(90))
RIGHT_ULTRASONIC = Ultrasonic(0, -constants.RIGHT_ULTRASONIC_OFFSET,
                              math.radians(-90))

ULTRASONICS = [FRONT_ULTRASONIC, LEFT_FRONT_ULTRASONIC, LEFT_BACK_ULTRASONIC,
                RIGHT_ULTRASONIC]

class SimRobotState:
    """
    Represents the state of the robot in the simulation, including its
    pose, wheel velocities, wheel positions, ultrasonic sensor readings, and
    time.
    """
    def __init__(self):
        self.pose = Pose2d(-0.2, -0.2, 0)

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
        
        self.ultrasonic_distances = [
            ultrasonic_distance_environment(self.pose, ultrasonic, envs.SIM_ENVIRONMENT)
            for ultrasonic in ULTRASONICS
        ]

        self.time = time
    
def ultrasonic_distance_wall(pose: Pose2d,
                             ultrasonic: Ultrasonic,
                             wall: envs.Wall) -> float:
    """
    Returns the distance from the ultrasonic sensor to the wall
    """

    # https://www.desmos.com/calculator/qxbd0xj5ar

    w_1x = wall.x1
    w_1y = wall.y1

    w_2x = wall.x2
    w_2y = wall.y2

    u_px = (pose.x + ultrasonic.x_offset * math.cos(pose.heading) 
                    - ultrasonic.y_offset * math.sin(pose.heading))
    u_py = (pose.y + ultrasonic.x_offset * math.sin(pose.heading)
                    + ultrasonic.y_offset * math.cos(pose.heading))

    u_theta = pose.heading + ultrasonic.heading_offset

    u_dx = math.cos(u_theta)
    u_dy = math.sin(u_theta)

    w_dx = w_2x - w_1x
    w_dy = w_2y - w_1y

    det = -u_dx * w_dy + u_dy * w_dx

    # Parallel to wall
    if abs(det) <= 1e-6:
        return math.inf 
    
    s_0 = ((w_1y-u_py)*(u_dx)+(w_1x-u_px)*(-u_dy)) / det

    # Goes outside range of wall
    if s_0 < 0 or s_0 > 1:
        return math.inf

    t_0 = ((w_1x-u_px)*(-w_dy) + (w_1y-u_py)*(w_dx)) / det

    # Pointing in wrong direction
    if t_0 < 0:
        return math.inf
    
    x_x = w_1x + s_0 * w_dx
    x_y = w_1y + s_0 * w_dy

    dist = math.sqrt((x_x - u_px)**2 + (x_y - u_py)**2)

    return dist

def ultrasonic_distance_environment(pose: Pose2d, 
                                    ultrasonic: Ultrasonic,
                                    environment: envs.Environment) -> float:
    """
    Returns the distance from the ultrasonic sensor to the closest wall in the
    environment.
    """
    min_dist = math.inf

    for wall in environment.get_walls():
        dist = ultrasonic_distance_wall(pose, ultrasonic, wall)
        min_dist = min(min_dist, dist)

    return min_dist