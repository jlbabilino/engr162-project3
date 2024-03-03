import math
import constants
from util import Pose2d, DriveWheelPositions

def inverse_kinematics(linear_velocity: float,
                       angular_velocity: float):
    left_speed = linear_velocity - (constants.TRACK_WIDTH / 2) * angular_velocity
    right_speed = linear_velocity + (constants.TRACK_WIDTH / 2) * angular_velocity
    return left_speed, right_speed

def forward_kinematics(prev_pose: Pose2d,
                       prev_wheel_positions: DriveWheelPositions,
                       curr_wheel_positions: DriveWheelPositions) -> Pose2d:
    left_distance = curr_wheel_positions.left - prev_wheel_positions.left
    right_distance = curr_wheel_positions.right - prev_wheel_positions.right
    
    distance = (left_distance + right_distance) / 2
    angle = (right_distance - left_distance) / constants.TRACK_WIDTH

    curr_x = prev_pose.x + math.cos(prev_pose.heading) * distance
    curr_y = prev_pose.y + math.sin(prev_pose.heading) * distance
    curr_heading = prev_pose.heading + angle

    return Pose2d(curr_x, curr_y, curr_heading)
