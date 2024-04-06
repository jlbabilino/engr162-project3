"""
Runnable script for the POC task 3. POC task 3 is to navigate the robot through
a grid of obstacles, which we hardcode since it was too difficult at the time.
"""

from robot_run_util import run_robot
from states.grid_nav_hardcode import GridNavHardcode

def main():
    run_robot(GridNavHardcode)

if __name__ == "__main__":
    main()
