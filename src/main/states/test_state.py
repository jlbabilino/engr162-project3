from robot_io import io
from robot import Robot

import math
from util import CardinalDirection

import commands.drive_forward_command as dfc
import commands.point_turn_command as ptc
import commands.turn_to_cardinal_direction_command as ttc
import commands.calibrate_heading_wall_command as chwc
import commands.calibrate_pos_wall_command as cpwc
import commands.sequential_command as sc
import commands.wait_command as wc
import commands.lambda_command as lc

import states.idle_state as ids

class TestState:
    def __init__(self, robot: Robot):
        self.robot = robot

        # self.command = sc.SequentialCommand([
        #     wc.WaitCommand(2),
        #     dfc.DriveForwardCommand(self.robot, 0, 0.4)
        # ])
        # self.command = sc.SequentialCommand([
        #     wc.WaitCommand(2),
        #     lc.LambdaCommand(lambda: io.drop_cargo()),
        # ])
        # self.command = ptc.PointTurnCommand(self.robot, math.radians(90))
        self.command = dfc.DriveForwardCommand(self.robot, 0, 0.4)
        self.command.initialize()

    def execute(self):
        if self.command.execute():
            return ids.IdleState(self.robot)
        else:
            return self