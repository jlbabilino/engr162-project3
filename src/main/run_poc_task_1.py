"""
Runnable script for the POC task 1. POC task 1 is to drive the robot straight
until it hits a wall.
"""

from robot_run_util import run_robot
from states.straight_until_wall_state import StraightUntilWallState

def main():
    run_robot(StraightUntilWallState, 0.0)

if __name__ == "__main__":
    main()
