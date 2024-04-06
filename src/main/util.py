import math
from dataclasses import dataclass

@dataclass
class DriveWheelPositions:
    """
    Represents the positions of the left and right drive wheels, as in the
    distance each wheel has traveled on the ground.
    """
    left: float
    right: float

@dataclass
class Translation2d:
    """
    Represents position in 2d space
    """
    x: float
    y: float

@dataclass
class Transform2d:
    translation: Translation2d
    rotation: float

@dataclass
class Pose2d:
    x: float
    y: float
    heading: float

    def __plus__(self, transform: Transform2d):
        # Adds the given transformation to the pose.
        # Adds the transform relative to the pose's frame of reference.
        dx = transform.translation.x
        dy = transform.translation.y
        theta = transform.rotation
        return Pose2d(
            self.x + dx * math.cos(self.heading)
                   - dy * math.sin(self.heading),
            self.y + dx * math.sin(self.heading)
                   + dy * math.cos(self.heading),
            self.heading + theta
        )
