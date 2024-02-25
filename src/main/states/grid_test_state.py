import math

from robot import Robot
from robot_io import io

import states.idle_state

import commands.drive_forward_command
import commands.point_turn_command
import commands.wait_command
import commands.sequential_command

# actions = ["f", "l", "f", "r", "f", "l"]
# actions = ["f", "r", "f", "f", "l"]
actions = ["f", "f", "f"]

class GridTestState:
    def __init__(self, robot: Robot):
        self.robot = robot
        self.commands = []

        curr_angle = 0.0
        for action in actions:
            if action == "l":
                curr_angle += math.radians(90)
            elif action == "r":
                curr_angle -= math.radians(90)
            self.commands.append(commands.point_turn_command.PointTurnCommand(self.robot, curr_angle))
            self.commands.append(commands.drive_forward_command.DriveForwardCommand(self.robot, curr_angle, 0.4))
            self.commands.append(commands.wait_command.WaitCommand(1))

        self.command = commands.sequential_command.SequentialCommand(self.commands)

        self.command.initialize()

    def execute(self):
        if (self.command.execute()):
            return states.idle_state.IdleState(self.robot)
        return self
