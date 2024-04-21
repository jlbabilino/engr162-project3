from robot import Robot
from robot_io import io

import states.idle_state as ids

from mapping.maze_map import MazeDecisionStatus

import states.command_then_state_state as cts
import states.detect_surroundings_state as dss
import states.attempt_drive_next_cell as adnc
import commands.sequential_command as sc
import commands.drive_in_cardinal_direction_command as dicdc
import commands.turn_to_cardinal_direction_command as ttc
import commands.lambda_command as lc

class DecideNextMoveState:
    def __init__(self, robot: Robot):
        self.robot = robot

    def execute(self):
        x = self.robot.coords.x
        y = self.robot.coords.y
        print(f"Current pose: ({x}, {y}, {self.robot.get_direction().name})")
        decision = self.robot.maze_map.optimal_next_move(x, y, self.robot.path)
        if decision.status == MazeDecisionStatus.EXIT:
            print("Exit found!")
            return cts.CommandThenStateState(
                sc.SequentialCommand([
                    lc.LambdaCommand(lambda: io.drop_cargo()),
                    lc.LambdaCommand(lambda: self.robot.maze_map.update_end_cell(x, y)),
                    lc.LambdaCommand(lambda: self.robot.maze_map.print())]),
                ids.IdleState(self.robot))
        elif decision.status == MazeDecisionStatus.STUCK:
            print("Stuck in maze...")
            return ids.IdleState(self.robot)
        elif decision.status == MazeDecisionStatus.BACKTRACK:
            print("Backtracking...")
            self.robot.path.pop()

            if decision.direction == self.robot.get_direction():
                return cts.CommandThenStateState(
                    dicdc.DriveInCardinalDirectionCommand(self.robot, False),
                    dss.DetectSurroundingsState(self.robot))
            elif decision.direction == self.robot.get_direction().reverse():
                return cts.CommandThenStateState(
                    dicdc.DriveInCardinalDirectionCommand(self.robot, True),
                    dss.DetectSurroundingsState(self.robot))
            else:
                return cts.CommandThenStateState(
                    sc.SequentialCommand([
                        ttc.TurnToCardinalDirectionCommand(self.robot, decision.direction),
                        dicdc.DriveInCardinalDirectionCommand(self.robot, False)]),
                    dss.DetectSurroundingsState(self.robot))
        elif decision.status == MazeDecisionStatus.NO_WALL_IN_WAY:
            print(f"Attempting move {decision.direction.name}")

            self.robot.path.append(decision.direction)

            if decision.direction == self.robot.get_direction():
                return adnc.AttemptDriveNextCell(self.robot)

            return cts.CommandThenStateState(
                        ttc.TurnToCardinalDirectionCommand(self.robot, decision.direction),
                        adnc.AttemptDriveNextCell(self.robot))
        else:
            return cts.CommandThenStateState(
                    ttc.TurnToCardinalDirectionCommand(self.robot, decision.direction),
                    dss.DetectSurroundingsState(self.robot))
