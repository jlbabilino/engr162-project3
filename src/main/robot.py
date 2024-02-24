from robot_io import io

class Robot:

    def __init__(self):
        self.heading_offset = 0.0
        self.target_heading = 0.0
        pass

    def initialize(self):
        self.heading_offset = io.gyro_angle()
        print("initialized")

    def get_heading(self):
        return io.gyro_angle() - self.heading_offset
    
    def set_target_heading(self, target_heading: float) -> None:
        self.target_heading = target_heading

    def get_target_heading(self) -> float:
        return self.target_heading

    def periodic(self):
        pass
