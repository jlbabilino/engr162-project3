import math

from robot import Robot
from robot_io import io
import states.closed_forward_state
import states.open_point_turn_state

class StraightUntilWallState:
    def __init__(self, robot: Robot, target_heading: float):
        self.robot = robot
        self.target_heading = target_heading # Assume pointed in right direction
        self.closed_forward_state = states.closed_forward_state.ClosedForwardState(self.robot, self.target_heading)

    def execute(self):

        self.closed_forward_state.execute()

        io.print_telemetry()
        if io.front_ultrasonic_distance() <= 0.09:
            print("Wall detected in front")
            if (io.left_front_ultrasonic_distance() <= 0.3): # must be a right turn
                print("Decided to make a right turn")
                self.target_heading += math.radians(-90)
                return states.open_point_turn_state.OpenPointTurnState(self.robot, self.target_heading, StraightUntilWallState(self.robot, self.target_heading))
            else:
                print("Decided to make a left turn")
                self.target_heading += math.radians(90)
                return states.open_point_turn_state.OpenPointTurnState(self.robot, self.target_heading, StraightUntilWallState(self.robot, self.target_heading))
        else:
            return self
