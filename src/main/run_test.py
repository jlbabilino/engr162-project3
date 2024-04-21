"""
Runnable python module that makes the robot go through the maze
"""

from robot_run_util import run_robot
from states.test_state import TestState
import states.attempt_drive_next_cell as adnc

def main():
    run_robot(adnc.AttemptDriveNextCell)

if __name__ == "__main__":
    main()
