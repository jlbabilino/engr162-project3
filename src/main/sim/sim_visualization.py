import math

import matplotlib.pyplot as plt

import constants
from util import Pose2d
from sim.sim_util import (Ultrasonic, SimRobotState,
                          ULTRASONICS)
import sim.sim_environments as envs

fig, ax = plt.subplots()

robot_marker = plt.Rectangle((0, 0),
                             constants.ROBOT_LENGTH,
                             constants.ROBOT_WIDTH,
                             angle=0,
                             rotation_point="center",
                             color='blue')

ax.add_patch(robot_marker)
ax.set_aspect('equal')

ax.set_xlim(-1, 1)
ax.set_ylim(-1, 1)

ax.grid(True)

# NUM_GRIDLINES_QUADRANT = 7
# ticks = [x * WALL_LENGTH for x in range(-NUM_GRIDLINES_QUADRANT,
#                                         +NUM_GRIDLINES_QUADRANT)]

# ax.set_xticks(ticks)
# ax.set_yticks(ticks)

def calc_ultrasonic_marker_coords(pose: Pose2d, ultrasonic: Ultrasonic,
                                  dist: float):
    x0 = pose.x + ultrasonic.x_offset * math.cos(pose.heading) - ultrasonic.y_offset * math.sin(pose.heading)
    y0 = pose.y + ultrasonic.x_offset * math.sin(pose.heading) + ultrasonic.y_offset * math.cos(pose.heading)
    x1 = x0 + dist * math.cos(pose.heading + ultrasonic.heading_offset)
    y1 = y0 + dist * math.sin(pose.heading + ultrasonic.heading_offset)

    return [x0, x1], [y0, y1]

ultrasonic_markers = []

for ultrasonic in ULTRASONICS:
    ultrasonic_markers.append(plt.Line2D(*calc_ultrasonic_marker_coords(Pose2d(0, 0, 0), ultrasonic, 0), color="lime"))
    ax.add_line(ultrasonic_markers[-1])

wall_markers = []

for wall in envs.SIM_ENVIRONMENT.get_walls():
    wall_markers.append(plt.Line2D([wall.x1, wall.x2], [wall.y1, wall.y2], color='black'))
    ax.add_line(wall_markers[-1])

ir_obstacle_markers = []

for obstacle in envs.SIM_ENVIRONMENT.get_ir_obstacles():
    ir_obstacle_markers.append(plt.Circle((obstacle.x, obstacle.y), 0.1, color='red'))
    ax.add_patch(ir_obstacle_markers[-1])

mag_obstacle_markers = []

for obstacle in envs.SIM_ENVIRONMENT.get_mag_obstacles():
    mag_obstacle_markers.append(plt.Circle((obstacle.x, obstacle.y), 0.1, color='purple'))
    ax.add_patch(mag_obstacle_markers[-1])

def initialize_viz():
    plt.ion()
    plt.show()

def update_viz(sim_robot_state: SimRobotState):
    robot_marker.set_xy((sim_robot_state.pose.x
                         - constants.ROBOT_LENGTH / 2,
                         sim_robot_state.pose.y
                         - constants.ROBOT_WIDTH / 2))
    robot_marker.set_angle(math.degrees(sim_robot_state.pose.heading))
    for i in range(len(ULTRASONICS)):
        distance = sim_robot_state.ultrasonic_distances[i]
        if distance == math.inf:
            distance = 10
        coords = calc_ultrasonic_marker_coords(
                sim_robot_state.pose,
                ULTRASONICS[i],
                distance)
        ultrasonic_markers[i].set_xdata(coords[0])
        ultrasonic_markers[i].set_ydata(coords[1])
    fig.canvas.draw()
    plt.pause(.001)