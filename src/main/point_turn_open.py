import math

from run_robot import run_robot
from states.open_point_turn_state import OpenPointTurnState

def main():
    angle = math.radians(float(input("Enter angle to turn (deg): ")))
    run_robot(OpenPointTurnState, angle)

if __name__ == "__main__":
    main()
