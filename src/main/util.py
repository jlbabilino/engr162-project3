from __future__ import annotations
import math
from enum import Enum
from dataclasses import dataclass

@dataclass
class Ultrasonic:
    """
    Represents an ultrasonic sensor on the robot
    """
    x_offset: float
    y_offset: float
    heading_offset: float

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
        return self.to_int_angle().to_angle()
        
    def plus(self, other_direction: CardinalDirection) -> CardinalDirection:
        """
        Adds two cardinal directions together.
        """

        angle_sum = self.value + other_direction.value
        return IntAngle(angle_sum).to_cardinal_direction()

    def reverse(self) -> CardinalDirection:
        if self == CardinalDirection.RIGHT:
            return CardinalDirection.LEFT
        elif self == CardinalDirection.UP:
            return CardinalDirection.DOWN
        elif self == CardinalDirection.LEFT:
            return CardinalDirection.RIGHT
        elif self == CardinalDirection.DOWN:
            return CardinalDirection.UP

    def to_int_angle(self) -> IntAngle:
        return IntAngle(self.value)

    @staticmethod
    def calc_rotation(robot: CardinalDirection, target: CardinalDirection) -> IntAngle:
        """
        Calculate the rotation needed to turn from the robot's current direction
        to the target direction.
        """
        diff = target.value - robot.value

        if diff == 3:
            return IntAngle(-1)
        elif diff == -3:
            return IntAngle(1)
        elif diff == -2:
            return IntAngle(2)
        else:
            return IntAngle(diff)
        
@dataclass
class IntAngle:
    angle: int

    def plus(self, other_angle: IntAngle):
        return IntAngle(self.angle + other_angle.angle)
    
    def to_cardinal_direction(self) -> CardinalDirection:
        cardinal_angle = self.angle

        if (cardinal_angle < -4):
            cardinal_angle = self.angle % -4
        elif (cardinal_angle > +4):
            cardinal_angle = self.angle % 4

        if (cardinal_angle == -4):
            cardinal_angle = 0
        elif (cardinal_angle == -3):
            cardinal_angle = 1
        elif (cardinal_angle == -2):
            cardinal_angle = 2
        elif (cardinal_angle == 3):
            cardinal_angle = -1
        elif (cardinal_angle == 4):
            cardinal_angle = 0

        return CardinalDirection(cardinal_angle)
    
    def to_angle(self) -> float:
        return self.angle * math.pi / 2

@dataclass
class MazeCoords:
    x: int
    y: int

    def move(self, direction: CardinalDirection) -> MazeCoords:
        if direction == CardinalDirection.RIGHT:
            return MazeCoords(self.x + 1, self.y)
        elif direction == CardinalDirection.UP:
            return MazeCoords(self.x, self.y + 1)
        elif direction == CardinalDirection.LEFT:
            return MazeCoords(self.x - 1, self.y)
        elif direction == CardinalDirection.DOWN:
            return MazeCoords(self.x, self.y - 1)
