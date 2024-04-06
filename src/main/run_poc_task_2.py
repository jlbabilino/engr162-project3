"""
Runnable script for the POC task 2. POC task 2 is to turn the robot in place by
a specified angle.
"""

import math

from robot_run_util import run_robot
from states.point_turn_state import PointTurnState

def main():
    angle = math.radians(float(input("Counter-clockwise angle (deg): ")))
    run_robot(PointTurnState, angle)

if __name__ == "__main__":
    main()
