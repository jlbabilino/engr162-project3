from __future__ import annotations
import math
from enum import Enum
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

class CardinalDirection(Enum):
    RIGHT = 0
    UP = 1
    DOWN = -1
    LEFT = 2

    def to_angle(self) -> float:
        if self == CardinalDirection.LEFT:
            return math.pi
        elif self == CardinalDirection.RIGHT:
            return 0
        elif self == CardinalDirection.UP:
            return math.pi / 2
        elif self == CardinalDirection.DOWN:
            return -math.pi / 2
        
    def add(self, other_direction: CardinalDirection) -> CardinalDirection:
        """
        Adds two cardinal directions together.
        """

        angle_sum = self.value + other_direction.value
        if angle_sum == -2:
            return CardinalDirection.LEFT
        elif angle_sum == 3:
            return CardinalDirection.DOWN
        elif angle_sum == 4:
            return CardinalDirection.RIGHT
        else:
            return CardinalDirection(angle_sum)
