import brickpi3
import grovepi

BP = brickpi3.BrickPi3()

try:
    while True:
        leftVal = grovepi.ultrasonicRead(3)
        rightVal = grovepi.ultrasonicRead(2)

        avg = leftVal
        # diff = (rightVal - leftVal)

        # print(f"Diff: {diff}")

        diff = 20 * (avg - 12)

        if diff < -600:
            diff = -600
        elif diff > 600:
            diff = 600

        print(f"avg: {avg}")
        BP.set_motor_dps(BP.PORT_B, 600 - diff)
        BP.set_motor_dps(BP.PORT_C, 600 + diff)

except KeyboardInterrupt as error:
    BP.reset_all()
