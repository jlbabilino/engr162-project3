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
        # REMOVE THIS LATER
        self.robot.x_coord += int(math.cos(self.robot.get_direction().to_angle()))
        self.robot.y_coord += int(math.sin(self.robot.get_direction().to_angle()))
        self.robot.maze_map.update_visited_cell(self.robot.x_coord, self.robot.y_coord)
        distances = {}
        distances[CardinalDirection.RIGHT] = (
                io.front_ultrasonic_distance()
                + constants.FRONT_ULTRASONIC_OFFSET)
        distances[CardinalDirection.DOWN] = (
                io.right_ultrasonic_distance()
                + constants.RIGHT_ULTRASONIC_OFFSET)
        distances[CardinalDirection.UP] = (
                0.5 * (io.left_front_ultrasonic_distance()
                     + io.left_back_ultrasonic_distance())
                     + constants.SIDE_ULTRASONIC_OFFSET)

        for direction, distance in distances.items():
            if distance < constants.WALL_DISTANCE:
                global_direction = self.robot.get_direction().add(direction)
                if self.robot.maze_map.get_wall(
                        self.robot.x_coord,
                        self.robot.y_coord,
                        global_direction) == None:
                    print("Detected wall at", direction, global_direction)
                    self.robot.maze_map.set_wall(
                            self.robot.x_coord, self.robot.y_coord, global_direction, True)

        self.robot.maze_map.pretty_print()
        return True

