from robot import Robot
from robot_io import io
from timer import Timer

class DriveForwardCommand:
    """
    Command to drive the robot forward a certain distance
    """
    def __init__(self, robot: Robot, target_heading: float, distance: float):
        """
        Create a DriveForwardCommand

        Args:
            robot: The robot object
            target_heading: The target heading to drive in direction of
            distance: The distance to drive (can be math.inf)
        """

        self.robot = robot
        self.target_heading = target_heading
        self.distance = distance
        
        self.velocity = 0.06
        
        self.drive_time = self.distance / self.velocity

        self.timer = Timer()

    def initialize(self):
        self.timer.start()

        print("DriveForwardCommand: Initialized")
        print(f"DriveForwardCommand: Distance = {self.distance:.3f} m")

    def execute(self) -> bool:
        error = self.robot.get_heading() - self.target_heading

        io.set_drive_left_speed(self.velocity + 0.5 * error)
        io.set_drive_right_speed(self.velocity - 0.5 * error)

        if self.timer.has_elapsed(self.drive_time):
            print(f"DriveForwardCommand: Done in {self.drive_time:.3f} s")
            io.set_drive_left_speed(0)
            io.set_drive_right_speed(0)
            return True
        return False
