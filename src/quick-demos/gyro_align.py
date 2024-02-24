import brickpi3

BP = brickpi3.BrickPi3()
BP.set_sensor_type(BP.PORT_1, BP.SENSOR_TYPE.EV3_GYRO_ABS_DPS)

try:
    while True:
        gyro_val = 0
        try:
            gyro_vals = BP.get_sensor(BP.PORT_1)
            print(f"Gyro Vals: {gyro_vals}")
            gyro_val = gyro_vals[0]
        except brickpi3.SensorError as error:
            print(error)
            continue

        print(f"Gyro: {gyro_val}")
        BP.set_motor_dps(BP.PORT_B, -gyro_val * 10)
        BP.set_motor_dps(BP.PORT_C, gyro_val * 10)

except KeyboardInterrupt as error:
    BP.reset_all()
