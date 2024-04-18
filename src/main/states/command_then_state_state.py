from robot import Robot
from robot_io import io

class CommandThenStateState:
    def __init__(self, command, state):

        self.command = command
        self.state = state

        self.command.initialize()

    def execute(self):
        if (self.command.execute()):
            return self.state
        else:
            return self
