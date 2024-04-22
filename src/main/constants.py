"""
Important physical constants of the GEARS.
"""

import math
from util import Ultrasonic

WHEEL_DIAMETER = 0.04 * (124 / 120)
WHEEL_GEAR_RATIO = 1 / 1

TRACK_WIDTH = 0.12

ROBOT_LENGTH = 0.18
ROBOT_WIDTH = 0.15

WALL_DISTANCE = 0.4

FRONT_ULTRASONIC = Ultrasonic(0.08, 0.045, 0)
RIGHT_FRONT_ULTRASONIC = Ultrasonic(0.065, -0.075, math.radians(-90))
RIGHT_BACK_ULTRASONIC = Ultrasonic(-0.065, -0.075, math.radians(-90))
LEFT_ULTRASONIC = Ultrasonic(0.025, 0.075, math.radians(90))

IR_THRESHOLD = 200
MAG_THRESHOLD = 1000