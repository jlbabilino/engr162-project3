from robot import Robot
from robot_io import io

def run_robot(initial_state_class) -> None:
    io.initialize_io()
    try:
        robot = Robot()

        robot.initialize()

        state = initial_state_class(robot)

        while True:
            robot.periodic()
            state = state.execute()

            # time.sleep(0.01)

    except KeyboardInterrupt as error:
        print("Aborting...")

    io.shutdown_io()
