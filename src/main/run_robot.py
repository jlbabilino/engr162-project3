from robot import Robot
import robot_io

def run_robot(initial_state_class) -> None:
    robot_io.initialize_io()
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

    robot_io.shutdown_io()
