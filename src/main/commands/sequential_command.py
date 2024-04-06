from robot import Robot
from robot_io import io
from timer import Timer

class SequentialCommand:
    """
    Command that runs a list of commands in order before terminating
    """
    def __init__(self, commands: list):
        self.commands = commands

        self.command_idx = 0

    def initialize(self):
        self.commands[0].initialize()

    def execute(self) -> bool:
        # Executes the commands in order, calling initialize() once per command before running
        # execute until it returns True. Once a command returns True, the next command is initialized
        # and executed.

        if self.command_idx < len(self.commands):
            if self.commands[self.command_idx].execute():
                self.command_idx += 1
                if self.command_idx < len(self.commands):
                    self.commands[self.command_idx].initialize()
                else:
                    return True
            return False
        else:
            return True
        
