from robot import Robot
from util import CardinalDirection

import commands.calibrate_heading_wall_command as chwc
import commands.calibrate_pos_wall_command as cpwc
import commands.sequential_command as sc
import commands.turn_to_cardinal_direction_command as ttc

import states.command_then_state_state as cts
import states.decide_next_move_state as dnms

class CalibrateState:

    def __init__(self, robot: Robot):
        self.robot = robot

    def execute(self):
        x = self.robot.coords.x
        y = self.robot.coords.y
        dir = self.robot.get_direction()
        right_wall_exists = self.robot.maze_map.get_wall_relative(
            x, y, dir, CardinalDirection.DOWN) # Direction of wall we care about
                                             # when robot is facing right
        front_wall_exists = self.robot.maze_map.get_wall_relative(
            x, y, dir, CardinalDirection.RIGHT)
        left_wall_exists = self.robot.maze_map.get_wall_relative(
            x, y, dir, CardinalDirection.UP)

        commands = []

        if right_wall_exists:
            commands.append(chwc.CalibrateHeadingWallCommand(self.robot))

        if front_wall_exists:
            commands.append(cpwc.CalibratePosWallCommand(self.robot))

        if right_wall_exists:
            commands.append(ttc.TurnToCardinalDirectionCommand(self.robot,
                                dir.plus(CardinalDirection.DOWN)))
            commands.append(cpwc.CalibratePosWallCommand(self.robot)) 

        if len(commands) == 0:
            return dnms.DecideNextMoveState(self.robot)
        else:
            return cts.CommandThenStateState(
                sc.SequentialCommand(commands),
                dnms.DecideNextMoveState(self.robot))
