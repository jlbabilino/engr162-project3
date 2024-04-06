import math

from robot_run_util import run_robot
from states.point_turn_state import PointTurnState

def main():
    angle = math.radians(float(input("Counter-clockwise angle (deg): ")))
    run_robot(PointTurnState, angle)

if __name__ == "__main__":
    main()
