"""
The interface to the simulated robot's sensors and motors. It is a drop-in
replacement for real_robot_io.py. Uses matplotlib to visualize the robot's
state and environment.
"""

import time as _time # Avoid name conflict with time module

from sim.sim_util import SimRobotState
import sim.sim_environments as envs
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

def left_front_ultrasonic_distance() -> float:
    return 100

def left_back_ultrasonic_distance() -> float:
    return 100

def front_ultrasonic_distance() -> float:
    return 100

def gyro_angle() -> bool:
    global sim_robot_state
    return sim_robot_state.get_pose().heading

def magnetic_obstacle_detected() -> bool:
    return False

def ir_obstacle_detected() -> bool:
    return False

def time() -> float:
    """
    Returns the time in seconds since the robot started
    """
    return (_time.time() - _initial_time)*3

# OUTPUTS
def set_drive_left_speed(wheel_tangential_velocity: float):
    global sim_robot_state

    sim_robot_state.set_left_wheel_velocity(wheel_tangential_velocity)

def set_drive_right_speed(wheel_tangential_velocity: float):
    global sim_robot_state

    sim_robot_state.set_right_wheel_velocity(wheel_tangential_velocity)

def print_telemetry():
    ...
