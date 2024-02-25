from robot import Robot
from robot_io import io

import states.idle_state
import commands.point_turn_command

class SimplePointTurnState:
    def __init__(self, robot: Robot, angle: float):
        self.robot = robot
        self.command = commands.point_turn_command.PointTurnCommand(self.robot, angle)
        self.command.initialize()

    def execute(self):
        if (self.command.execute()):
            return states.idle_state.IdleState(self.robot)
        return self