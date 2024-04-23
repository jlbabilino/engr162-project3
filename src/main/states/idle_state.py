import constants
import time

from robot import Robot
from robot_io import io

class IdleState:
    """
    In this state, robot does nothing. Useful for debugging, testing, etc.
    """
    def __init__(self, robot: Robot):
        self.robot = robot

    def execute(self):
        io.print_telemetry()
        time.sleep(0.1)
        # io.magnetic_obstacle_detected()

        # print(f"Magnet: {io.magnetic_reading():6.3f} IR: {io.ir_reading():6.3f}")

        # print(f"Right: {(0.5 * (io.right_front_ultrasonic_distance() + io.right_back_ultrasonic_distance()) - constants.RIGHT_FRONT_ULTRASONIC.y_offset):6.3f} Front: {(io.front_ultrasonic_distance() + constants.FRONT_ULTRASONIC.x_offset):6.3f}")

        return self