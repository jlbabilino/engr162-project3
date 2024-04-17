import math

from robot import Robot
from util import CardinalDirection
import commands.sequential_command as sc
import commands.point_turn_command as ptc
import commands.lambda_command as lc

class TurnToCardinalDirectionCommand:
    """
    Command to turn the robot to a certain cardinal direction
    """
    def __init__(self, robot: Robot, target_direction: CardinalDirection):
        self.robot = robot

        self.target_direction = target_direction

        self.point_turn_command = ptc.PointTurnCommand(robot, target_direction.to_angle())
        self.set_dir_command = lc.LambdaCommand(lambda: self.robot.set_direction(self.target_direction))
        self.seq_command = sc.SequentialCommand([self.point_turn_command, self.set_dir_command])

    def initialize(self):
        self.point_turn_command.initialize()

    def execute(self) -> bool:
        return self.seq_command.execute()

