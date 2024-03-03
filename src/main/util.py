from dataclasses import dataclass

@dataclass
class DriveWheelPositions:
    left: float
    right: float

@dataclass
class Pose2d:
    x: float
    y: float
    heading: float
