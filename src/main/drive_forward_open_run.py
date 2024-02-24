from run_robot import run_robot
from states.open_forward_state import OpenForwardState

def main():
    run_robot(OpenForwardState, 0.2)

if __name__ == "__main__":
    main()
