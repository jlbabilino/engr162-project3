import math

from run_robot import run_robot
from states.open_point_turn_state import OpenPointTurnState

def main():
    run_robot(OpenPointTurnState)

if __name__ == "__main__":
    main()
