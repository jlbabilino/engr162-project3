"""
Moves the robot forward and then rotates, then repeats.
"""

import time

import brickpi3

BP = brickpi3.BrickPi3()

try:
    while True:
        BP.set_motor_dps(BP.PORT_B, -200)
        BP.set_motor_dps(BP.PORT_C, 200)
        time.sleep(1)
        BP.set_motor_dps(BP.PORT_B, 200)
        BP.set_motor_dps(BP.PORT_C, 200)
        time.sleep(1)
except KeyboardInterrupt as error:
    BP.reset_all()
