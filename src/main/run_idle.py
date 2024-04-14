"""
Runnable python module that makes the robot do absolutely nothing.
Useful for testing the robot's sensors and motors.
"""

from robot_run_util import run_robot
from states.idle_state import IdleState

def main():
    run_robot(IdleState)

if __name__ == "__main__":
    main()
