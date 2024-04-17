import math

from robot import Robot
from robot_io import io

import states.idle_state

import commands.drive_forward_command
import commands.turn_to_cardinal_direction_command as tcd
import commands.wait_command
import commands.sequential_command
import commands.detect_surroundings_command

from util import CardinalDirection

# actions = ["f", "l", "l", "l", "f"]
# actions = ["f", "r", "f", "f", "l"]
# actions = ["f", "f", "f"]

actions = ["r", "r", "l", "d", "d", "r", "r", "u", "r", "r", "d", "r", "r",
           "r", "u", "l", "u", "l", "l", "d", "l", "l", "d", "l", "d", "d",
           "d", "d", "r", "r", "u", "u", "l", "r", "d", "r", "r", "r", "r",
           "u", "u", "d", "r", "l", "d", "d", "r", "r", "r", "r"]
# actions = ["p", "p"]

class GridNavHardcode:
    """
    This state is used to hardcode a path for the robot to follow. It uses a
    sequence of commands.
    """
    def __init__(self, robot: Robot):
        self.robot = robot
        self.commands = []

        for action in actions:
            direction = None
            if action == "l":
                direction = CardinalDirection.LEFT
            elif action == "r":
                direction = CardinalDirection.RIGHT
            elif action == "u":
                direction = CardinalDirection.UP
            elif action == "d":
                direction = CardinalDirection.DOWN
            self.commands.append(tcd.TurnToCardinalDirectionCommand(self.robot, direction))
            self.commands.append(commands.drive_forward_command.DriveForwardCommand(self.robot, direction.to_angle(), 0.4))
            self.commands.append(commands.wait_command.WaitCommand(1))
            self.commands.append(commands.detect_surroundings_command.DetectSurroundingsCommand(self.robot))

        self.command = commands.sequential_command.SequentialCommand(self.commands)

        self.command.initialize()

    def execute(self):
        if (self.command.execute()):
            return states.idle_state.IdleState(self.robot)
        return self
