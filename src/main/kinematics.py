import math
import constants
from util import Pose2d, DriveWheelPositions

def inverse_kinematics(linear_velocity: float,
                       angular_velocity: float):
    left_speed = linear_velocity - (constants.TRACK_WIDTH / 2) * angular_velocity
    right_speed = linear_velocity + (constants.TRACK_WIDTH / 2) * angular_velocity
    return left_speed, right_speed

# def forward_kinematics(left_distance: float, right_distance: float):
#     distance = (left_distance + right_distance) / 2
#     angle = (right_distance - left_distance) / constants.TRACK_WIDTH
#     return distance, angle

def forward_kinematics(prev_pose: Pose2d,
                       prev_wheel_positions: DriveWheelPositions,
                       curr_wheel_positions: DriveWheelPositions) -> Pose2d:
    left_distance = curr_wheel_positions.left - prev_wheel_positions.left
    right_distance = curr_wheel_positions.right - prev_wheel_positions.right
    
    distance = (left_distance + right_distance) / 2
    angle = (right_distance - left_distance) / constants.TRACK_WIDTH

    # Courtesy of: https://github.com/wpilibsuite/allwpilib/blob/e64c20346dfe3252098f0efe51a93bb766881b82/wpimath/src/main/java/edu/wpi/first/math/geometry/Pose2d.java#L219-L242
    
    sinTheta = math.sin(angle);
    cosTheta = math.cos(angle);

    s = 0
    c = 0
    if abs(angle) < 1E-9:
      s = 1 - 1 / 6 * angle ** 2
      c = 0.5 * angle
    else:
      s = sinTheta / angle
      c = (1 - cosTheta) / angle

    curr_x = prev_pose.x + distance * s
    curr_y = prev_pose.y + distance * c
    curr_heading = prev_pose.heading + angle

    return Pose2d(curr_x, curr_y, curr_heading)
