import math
from robot import Robot
from robot_io import io
import constants
from util import CardinalDirection

class DetectSurroundingsCommand:
    """
    This command is used to detect walls and obstacles around the robot.
    """
    def __init__(self, robot: Robot):
        self.robot = robot

    def initialize(self):
        pass

    def execute(self):
        distances = {}
        distances[CardinalDirection.RIGHT] = (
                io.front_ultrasonic_distance()
                + constants.FRONT_ULTRASONIC.x_offset)
        distances[CardinalDirection.DOWN] = (
                0.5 * (io.right_front_ultrasonic_distance()
                     + io.right_back_ultrasonic_distance())
                     - constants.RIGHT_FRONT_ULTRASONIC.y_offset)
        # distances[CardinalDirection.UP] = (
        #         io.left_ultrasonic_distance()
        #         + constants.LEFT_ULTRASONIC.y_offset)

        for direction, distance in distances.items():
            global_direction = self.robot.get_direction().plus(direction)
            # if self.robot.maze_map.get_wall(
            #             self.robot.coords.x,
            #             self.robot.coords.y,
            #             global_direction) == None:
            if distance < constants.WALL_DISTANCE:
                self.robot.maze_map.set_wall(
                        self.robot.coords.x, self.robot.coords.y, global_direction, True)
            else:
                self.robot.maze_map.set_wall(
                        self.robot.coords.x, self.robot.coords.y, global_direction, False)

        self.robot.maze_map.pretty_print()
        return True

