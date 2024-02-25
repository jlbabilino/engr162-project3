from run_robot import run_robot
from states.straight_until_wall_state import StraightUntilWallState

def main():
    run_robot(StraightUntilWallState, 0.0)

if __name__ == "__main__":
    main()
