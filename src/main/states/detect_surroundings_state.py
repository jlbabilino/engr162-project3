from robot import Robot

import states.command_then_state_state as cts

import commands.detect_surroundings_command as dsc
import states.calibrate_state as cs

def DetectSurroundingsState(robot: Robot) -> cts.CommandThenStateState:
    return cts.CommandThenStateState(
            dsc.DetectSurroundingsCommand(robot),
            cs.CalibrateState(robot))