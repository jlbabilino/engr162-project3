import math

import matplotlib.pyplot as plt

import constants
from sim.sim_util import Environment, SimRobotState
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

ultrasonic_markers = []

# for ultrasonic in [front_ultrasonic, left_front_ultrasonic, left_back_ultrasonic]:
#     ultrasonic_markers.append(plt.Line2D([0, ultrasonic.x_offset], [0, ultrasonic.y_offset], color='red'))
#     ax.add_line(ultrasonic_markers[-1])

wall_markers = []

for wall in envs.SIM_ENVIRONMENT.get_walls():
    wall_markers.append(plt.Line2D([wall.x1, wall.x2], [wall.y1, wall.y2], color='black'))
    ax.add_line(wall_markers[-1])

def initialize_viz():
    plt.ion()
    plt.show()

def update_viz(sim_robot_state: SimRobotState):
    robot_marker.set_xy((sim_robot_state.get_pose().x - constants.ROBOT_LENGTH / 2, sim_robot_state.get_pose().y - constants.ROBOT_WIDTH / 2))
    robot_marker.set_angle(math.degrees(sim_robot_state.get_pose().heading))
    fig.canvas.draw()
    plt.pause(.001)