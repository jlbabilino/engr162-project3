"""
The interface to the simulated robot's sensors and motors.
"""

import matplotlib.pyplot as plt
import math
import time as _time # Avoid name conflict with time module

import constants
from sim.sim_manager import SimRobotState

fig, ax = plt.subplots()

robot_marker = plt.Rectangle((0, 0), 1, 1, angle=40, rotation_point="center", color='blue')

ax.add_patch(robot_marker)
ax.set_aspect('equal')

ax.set_xlim(-5, 5)
ax.set_ylim(-5, 5)

# Keep track of timestamp robot starts at
_initial_time = 0.0
sim_robot_state = SimRobotState()

def initialize():
    global _initial_time # Python requires this to modify global variable
    # Initialize timestamp so that time() returns 0 at the start of the program
    _initial_time = _time.time()

    plt.ion()
    plt.show()

def periodic():
    global sim_robot_state
    sim_robot_state.update(time())
    robot_marker.set_xy((sim_robot_state.get_pose().x, sim_robot_state.get_pose().y))
    robot_marker.set_angle(math.degrees(sim_robot_state.get_pose().heading))
    fig.canvas.draw()
    plt.pause(.001)

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
    return _time.time() - _initial_time

# OUTPUTS
def set_drive_left_speed(wheel_tangential_velocity: float):
    global sim_robot_state

    sim_robot_state.set_left_wheel_velocity(wheel_tangential_velocity)


def set_drive_right_speed(wheel_tangential_velocity: float):
    global sim_robot_state

    sim_robot_state.set_right_wheel_velocity(wheel_tangential_velocity)

def print_telemetry():
    print("Telemetry")
