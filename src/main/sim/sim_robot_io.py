"""
The interface to the simulated robot's sensors and motors.
"""

import matplotlib.pyplot as plt
import math
import time as _time # Avoid name conflict with time module

import constants
from sim.sim_manager import SimRobotState, Environment, Wall, Ultrasonic, sim_environment

fig, ax = plt.subplots()

robot_marker = plt.Rectangle((0, 0), constants.ROBOT_LENGTH, constants.ROBOT_WIDTH, angle=0, rotation_point="center", color='blue')

ax.add_patch(robot_marker)
ax.set_aspect('equal')

ax.set_xlim(-1, 1)
ax.set_ylim(-1, 1)

ax.grid(True)
ax.set_xticks([-1, -0.6, -0.2, 0.2, 0.6, 1])
ax.set_yticks([-1, -0.6, -0.2, 0.2, 0.6, 1])

# Keep track of timestamp robot starts at
_initial_time = 0.0
sim_robot_state = SimRobotState()

ultrasonic_markers = []

# for ultrasonic in [front_ultrasonic, left_front_ultrasonic, left_back_ultrasonic]:
#     ultrasonic_markers.append(plt.Line2D([0, ultrasonic.x_offset], [0, ultrasonic.y_offset], color='red'))
#     ax.add_line(ultrasonic_markers[-1])

wall_markers = []

for wall in sim_environment.get_walls():
    wall_markers.append(plt.Line2D([wall.x1, wall.x2], [wall.y1, wall.y2], color='black'))
    ax.add_line(wall_markers[-1])

def initialize():
    global _initial_time # Python requires this to modify global variable
    # Initialize timestamp so that time() returns 0 at the start of the program
    _initial_time = _time.time()

    plt.ion()
    plt.show()

def periodic():
    global sim_robot_state
    sim_robot_state.update(time())
    robot_marker.set_xy((sim_robot_state.get_pose().x - constants.ROBOT_LENGTH / 2, sim_robot_state.get_pose().y - constants.ROBOT_WIDTH / 2))
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
    return (_time.time() - _initial_time)*10

# OUTPUTS
def set_drive_left_speed(wheel_tangential_velocity: float):
    global sim_robot_state

    sim_robot_state.set_left_wheel_velocity(wheel_tangential_velocity)

def set_drive_right_speed(wheel_tangential_velocity: float):
    global sim_robot_state

    sim_robot_state.set_right_wheel_velocity(wheel_tangential_velocity)

def print_telemetry():
    print("Telemetry")
