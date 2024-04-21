import math

from robot import Robot
from robot_io import io

import states.turn_then_straight_state as sts
import commands.drive_forward_command as cmds

class StraightUntilWallState:
    """
    This state goes straight until a wall is detected in front of the robot.
    In that case it checks whether it should go left or right, depending on
    what it detects to the sides.
    """
    def __init__(self, robot: Robot, target_heading: float):
        self.robot = robot
        self.target_heading = target_heading

        self.drive_command = cmds.DriveForwardCommand(self.robot,
                                                     self.target_heading,
                                                     +math.inf)

        self.drive_command.initialize()

    def execute(self):
        self.drive_command.execute()

        io.print_telemetry()
        if io.left_ultrasonic_distance() <= 0.09:
            print("StraightUntilWallState: Wall detected in front")
            if (io.right_front_ultrasonic_distance() <= 0.3): # must be a right turn
                print("StraightUntilWallState: Decided to make a right turn")
                self.target_heading += math.radians(-90)
            else:
                print("StraightUntilWallState: Decided to make a left turn")
                self.target_heading += math.radians(90)
            return sts.TurnThenStraightState(self.robot, self.target_heading)
        else:
            return self
