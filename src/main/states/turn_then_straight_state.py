from robot import Robot
import states.straight_until_wall_state
import commands.point_turn_command

class TurnThenStraightState:
    """
    This state starts by turning the robot to a target heading, and then
    transitions to going straight again.
    """
    def __init__(self, robot: Robot, target_heading: float):
        self.robot = robot
        self.target_heading = target_heading

        self.turn_command = commands.point_turn_command.PointTurnCommand(self.robot, self.target_heading)

        self.turn_command.initialize()

    def execute(self):
        if (self.turn_command.execute()):
            return states.straight_until_wall_state.StraightUntilWallState(self.robot, self.target_heading)
        else:
            return self
