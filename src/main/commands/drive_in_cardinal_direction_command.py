import math

import constants
from robot import Robot
from util import CardinalDirection
import commands.sequential_command as sc
import commands.drive_forward_command as dfc
import commands.lambda_command as lc

class DriveInCardinalDirectionCommand:
    """
    Command to drive the robot in a cardinal direction, one grid space (40 cm)
    """
    def __init__(self, robot: Robot, target_direction: CardinalDirection):
        self.robot = robot

        self.target_direction = target_direction

        self.drive_command = dfc.DriveForwardCommand(
                robot, target_direction.to_angle(), constants.WALL_DISTANCE)
        def update_coords():
            self.robot.set_maze_coords(self.robot.get_maze_coords().move(self.target_direction))
            self.robot.maze_map.update_visited_cell(self.robot.get_maze_coords().x, self.robot.get_maze_coords().y)
        self.set_coords_command = lc.LambdaCommand(update_coords)
        self.seq_command = sc.SequentialCommand([self.drive_command, self.set_coords_command])

    def initialize(self):
        self.drive_command.initialize()

    def execute(self) -> bool:
        return self.seq_command.execute()

