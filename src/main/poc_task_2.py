import math

from run_robot import run_robot
from states.simple_point_turn_state import SimplePointTurnState

def main():
    angle = math.radians(float(input("Counter-clockwise angle (deg): ")))
    run_robot(SimplePointTurnState, angle)

if __name__ == "__main__":
    main()
