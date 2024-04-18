"""
Runnable python module that makes the robot go through the maze
"""

from robot_run_util import run_robot
from states.detect_surroundings_state import DetectSurroundingsState

def main():
    run_robot(DetectSurroundingsState)

if __name__ == "__main__":
    main()
