import constants

def inverse_kinematics(linear_velocity: float,
                       angular_velocity: float):
    left_speed = linear_velocity - (constants.TRACK_WIDTH / 2) * angular_velocity
    right_speed = linear_velocity + (constants.TRACK_WIDTH / 2) * angular_velocity
    return left_speed, right_speed