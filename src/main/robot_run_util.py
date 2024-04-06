import math

from robot import Robot
from robot_io import io

def run_robot(initial_state_class, *state_args) -> None:
    """
    Begin running the robot with some initial state.

    Args:
        initial_state_class: The initial state class to start the robot in.
        state_args: The arguments to pass to the initial state class
                    constructor.
    """
    io.initialize()
    try:
        robot = Robot()

        robot.initialize()

        state = initial_state_class(robot, *state_args)

        while True:
            robot.periodic()
            io.periodic()

            state = state.execute()

            # time.sleep(0.01)

    except KeyboardInterrupt as error:
        print("Aborting...")

    io.shutdown()
