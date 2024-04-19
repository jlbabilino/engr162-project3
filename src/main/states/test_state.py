from robot import Robot

from util import CardinalDirection

import commands.drive_in_cardinal_direction_command as dicdc
import commands.turn_to_cardinal_direction_command as ttc
import commands.sequential_command as sc

import states.idle_state as ids

class TestState:
    def __init__(self, robot: Robot):
        self.robot = robot

        self.command = sc.SequentialCommand([
            dicdc.DriveInCardinalDirectionCommand(robot),
            ttc.TurnToCardinalDirectionCommand(robot, CardinalDirection.UP),
            dicdc.DriveInCardinalDirectionCommand(robot),
        ])
        self.command.initialize()

    def execute(self):
        if self.command.execute():
            return ids.IdleState(self.robot)
        else:
            return self