from robot import Robot
from robot_io import io
from timer import Timer

class WaitCommand:
    def __init__(self, duration: float):
        self.duration = duration
        self.timer = Timer()

    def initialize(self):
        self.timer.start()

    def execute(self) -> bool:
        return self.timer.has_elapsed(self.duration)
