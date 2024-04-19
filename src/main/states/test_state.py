from robot import Robot

from util import CardinalDirection

import commands.drive_forward_command as dfc
import commands.turn_to_cardinal_direction_command as ttc
import commands.sequential_command as sc

import states.idle_state as ids

class TestState:
    def __init__(self, robot: Robot):
        self.robot = robot

        self.command = sc.SequentialCommand([
            ttc.TurnToCardinalDirectionCommand(self.robot, CardinalDirection.UP),
            dfc.DriveForwardCommand(self.robot, 3.141592/2, +0.40),
        ])
        self.command.initialize()

    def execute(self):
        if self.command.execute():
            return ids.IdleState(self.robot)
        else:
            return self