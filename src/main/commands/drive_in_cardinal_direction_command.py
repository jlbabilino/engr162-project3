import math

import constants
from robot import Robot
from robot_io import io
from util import CardinalDirection
import commands.sequential_command as sc
import commands.drive_forward_command as dfc
import commands.lambda_command as lc

class DriveInCardinalDirectionCommand:
    """
    Command to drive the robot in a cardinal direction, one grid space (40 cm)
    """
    def __init__(self, robot: Robot, reverse: bool = False):
        self.robot = robot
        self.reverse = reverse

    def initialize(self):
        self.target_heading = self.robot.get_heading_int_angle().to_angle()
        self.target_direction = self.robot.get_direction()

        dist = constants.WALL_DISTANCE
        if self.reverse:
            dist = -dist

        self.drive_command = dfc.DriveForwardCommand(
                self.robot, self.target_heading, dist)

        def update_coords():
            move_dir = self.target_direction
            if self.reverse:
                move_dir = move_dir.reverse()
            self.robot.set_maze_coords(self.robot.get_maze_coords().move(move_dir))
            self.robot.maze_map.update_visited_cell(self.robot.get_maze_coords().x, self.robot.get_maze_coords().y)

        self.set_coords_command = lc.LambdaCommand(update_coords)
        self.seq_command = sc.SequentialCommand([self.drive_command, self.set_coords_command])

        self.drive_command.initialize()

    def execute(self) -> bool:
        print(f"Mag: {io.magnetic_reading()}")
        return self.seq_command.execute()

