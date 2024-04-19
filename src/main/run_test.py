"""
Runnable python module that makes the robot go through the maze
"""

from robot_run_util import run_robot
from states.test_state import TestState

def main():
    run_robot(TestState)

if __name__ == "__main__":
    main()
