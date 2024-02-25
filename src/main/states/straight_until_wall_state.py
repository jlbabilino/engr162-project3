import math

from robot import Robot
from robot_io import io
import states.closed_forward_state
import states.open_point_turn_state

import states.turn_then_straight_state
import commands.drive_forward_command

class StraightUntilWallState:
    def __init__(self, robot: Robot, target_heading: float):
        self.robot = robot
        self.target_heading = target_heading

        self.drive_command = commands.drive_forward_command.DriveForwardCommand(self.robot, self.target_heading, 10)

        self.drive_command.initialize()

    def execute(self):
        self.drive_command.execute()

        io.print_telemetry()
        if io.front_ultrasonic_distance() <= 0.09:
            print("Wall detected in front")
            if (io.left_front_ultrasonic_distance() <= 0.3): # must be a right turn
                print("Decided to make a right turn")
                self.target_heading += math.radians(-90)
            else:
                print("Decided to make a left turn")
                self.target_heading += math.radians(90)
            return states.turn_then_straight_state.TurnThenStraightState(self.robot, self.target_heading)
        else:
            return self
