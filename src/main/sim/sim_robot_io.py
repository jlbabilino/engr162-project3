"""
The interface to the simulated robot's sensors and motors. It is a drop-in
replacement for real_robot_io.py. Uses matplotlib to visualize the robot's
state and environment.
"""

import math
import time as _time # Avoid name conflict with time module

from sim.sim_util import SimRobotState
import sim.sim_visualization as viz

# Keep track of timestamp robot starts at
_initial_time = 0.0
sim_robot_state = SimRobotState()

def initialize():
    global _initial_time # Python requires this to modify global variable
    # Initialize timestamp so that time() returns 0 at the start of the program
    _initial_time = _time.time()

    viz.initialize_viz()

def periodic():
    global sim_robot_state
    sim_robot_state.update(time())
    viz.update_viz(sim_robot_state)

def shutdown():
    pass

def front_ultrasonic_distance() -> float:
    global sim_robot_state
    return round(sim_robot_state.ultrasonic_distances[0], 2)

def right_front_ultrasonic_distance() -> float:
    global sim_robot_state
    return round(sim_robot_state.ultrasonic_distances[1], 2)

def right_back_ultrasonic_distance() -> float:
    global sim_robot_state
    return round(sim_robot_state.ultrasonic_distances[2], 2)

def left_ultrasonic_distance() -> float:
    global sim_robot_state
    return sim_robot_state.ultrasonic_distances[3]

def gyro_angle() -> bool:
    global sim_robot_state
    return sim_robot_state.pose.heading * 1

def magnetic_reading() -> float:
    global sim_robot_state
    return sim_robot_state.mag_reading

def ir_reading() -> float:
    global sim_robot_state
    return sim_robot_state.ir_reading

def time() -> float:
    """
    Returns the time in seconds since the robot started
    """
    return (_time.time() - _initial_time)*3

# OUTPUTS
def set_drive_left_speed(wheel_tangential_velocity: float):
    global sim_robot_state

    sim_robot_state.left_wheel_velocity = wheel_tangential_velocity

def set_drive_right_speed(wheel_tangential_velocity: float):
    global sim_robot_state

    sim_robot_state.right_wheel_velocity = wheel_tangential_velocity

def stow_cargo():
    pass

def drop_cargo():
    pass

def print_telemetry():
    ...
