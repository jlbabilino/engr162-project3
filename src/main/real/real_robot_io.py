"""
The interface to the real robot's sensors and motors.
"""

import math
import time as _time # Avoid name conflict with time module

import brickpi3
import grovepi
from real.MPU9250 import MPU9250 # IMU library

import constants

# Initialize BrickPi3 and MPU9250 libraries
BP = brickpi3.BrickPi3()
mpu9250 = MPU9250()

# LEGO Sensor Ports
GYRO_PORT = BP.PORT_4
LEFT_ULTRASONIC_PORT = BP.PORT_3

# GrovePi Sensor Ports
RIGHT_FRONT_ULTRASONIC_PORT = 3
RIGHT_BACK_ULTRASONIC_PORT = 2
FRONT_ULTRASONIC_PORT = 4
IR_LEFT_PORT = 15 # These are for port A0
IR_RIGHT_PORT = 14

# LEGO Motor Ports
DRIVE_LEFT_PORT = BP.PORT_B
DRIVE_RIGHT_PORT = BP.PORT_C
CARGO_PORT = BP.PORT_A

# Keep track of timestamp robot starts at
_initial_time = 0.0

def initialize():
    """
    Initializes the LEGO sensors and motors and GrovePi sensors
    """
    # Initialize LEGO sensors
    BP.set_sensor_type(GYRO_PORT, BP.SENSOR_TYPE.EV3_GYRO_ABS_DPS)
    BP.set_sensor_type(FRONT_ULTRASONIC_PORT, BP.SENSOR_TYPE.EV3_ULTRASONIC_CM)

    # Clear errors for LEGO sensors
    print("Calibrating Gyro...")
    gyro_angle()
    print("Gyro Calibrated!")
    print("Calibrating Front Ultrasonic...")
    left_ultrasonic_distance()
    print("Front Ultrasonic Calibrated!")

    # Reset motor encoders
    BP.offset_motor_encoder(
            DRIVE_LEFT_PORT, BP.get_motor_encoder(DRIVE_LEFT_PORT))
    BP.offset_motor_encoder(
            DRIVE_RIGHT_PORT, BP.get_motor_encoder(DRIVE_RIGHT_PORT))
    BP.offset_motor_encoder(
            CARGO_PORT, BP.get_motor_encoder(CARGO_PORT))
    
    stow_cargo()
    print("Load cargo now!")
    _time.sleep(4)

    global _initial_time # Python requires this to modify global variable
    # Initialize timestamp so that time() returns 0 at the start of the program
    _initial_time = _time.time()

def periodic():
    pass

def shutdown():
    """
    Shuts down the LEGO sensors and motors and GrovePi sensors
    """
    # Kill all motors and sensors
    BP.reset_all()

def right_front_ultrasonic_distance() -> float:
    """
    Returns the distance in meters from the left front ultrasonic sensor
    """
    return grovepi.ultrasonicRead(RIGHT_FRONT_ULTRASONIC_PORT) / 100 # cm -> m

def right_back_ultrasonic_distance() -> float:
    """
    Returns the distance in meters from the right back ultrasonic sensor
    """
    return grovepi.ultrasonicRead(RIGHT_BACK_ULTRASONIC_PORT) / 100 # cm -> m

def left_ultrasonic_distance() -> float:
    """
    Returns the distance in meters from the left ultrasonic sensor
    """
    # Keep iterating until no error happens
    while True:
        try:
            return BP.get_sensor(LEFT_ULTRASONIC_PORT) / 100 # cm -> m
        except brickpi3.SensorError as error:
            pass

def front_ultrasonic_distance() -> float:
    """
    Returns the distance in meters from the left back ultrasonic sensor
    """
    return grovepi.ultrasonicRead(FRONT_ULTRASONIC_PORT) / 100 # cm -> m

def gyro_angle() -> bool:
    """
    Returns the heading of the robot from the gyro, in radians
    """
    # In test:
    # Target: 360*20 deg
    # Actual: 360*20 + 19
    # It went too far, so scale down reported value


    # Keep iterating until no error happens
    while True:
        try:
            # Get the gyro angle from pair of (angle, rate)
            # Convert to radians, use counter-clockwise as positive
            # return ((360*20) / (360*20 + 19)) * -math.radians(BP.get_sensor(GYRO_PORT)[0])
            return -math.radians(BP.get_sensor(GYRO_PORT)[0])
        except brickpi3.SensorError as error:
            pass

# Cache previous magnet reading
_previous_magnet_reading = (0, 0, 0)

def magnetic_reading() -> float:
    """
    Check if a magnetic obstacle is in front of the robot
    """
    global _previous_magnet_reading
    # new_magnet_reading = math.sqrt(mpu9250.readMagnet()["x"]**2
    #                              + mpu9250.readMagnet()["y"]**2
    #                              + mpu9250.readMagnet()["z"]**2)
    raw_reading = mpu9250.readMagnet()
    new_magnet_reading = (raw_reading["x"], raw_reading["y"], raw_reading["z"])
    if new_magnet_reading[0] != 0:
        _previous_magnet_reading = new_magnet_reading
        # print(f"Magnet: {new_magnet_reading}")

    return _previous_magnet_reading[2]

def ir_reading() -> float:
    """
    Check if an IR obstacle is in front of the robot
    """

    avg_ir = 0.5 * (grovepi.analogRead(IR_LEFT_PORT)
                  + grovepi.analogRead(IR_RIGHT_PORT))
    return avg_ir

def time() -> float:
    """
    Returns the time in seconds since the robot started
    """
    return _time.time() - _initial_time

# OUTPUTS
def set_drive_left_speed(wheel_tangential_velocity: float):
    """
    Sets the tangential velocity of the left wheel
    """
    wheel_angular_speed = wheel_tangential_velocity / (
            constants.WHEEL_DIAMETER / 2)
    BP.set_motor_dps(DRIVE_LEFT_PORT,
                     math.degrees(wheel_angular_speed)
                     * constants.WHEEL_GEAR_RATIO)

def set_drive_right_speed(wheel_tangential_velocity: float):
    """
    Sets the tangential velocity of the right wheel
    """
    wheel_angular_speed = wheel_tangential_velocity / (
            constants.WHEEL_DIAMETER / 2)
    BP.set_motor_dps(DRIVE_RIGHT_PORT,
                     -math.degrees(wheel_angular_speed)
                     * constants.WHEEL_GEAR_RATIO)
    
def stow_cargo():
    BP.set_motor_position(CARGO_PORT, -20)

def drop_cargo():
    BP.set_motor_position(CARGO_PORT, -130)

def print_telemetry():
    """
    Prints telemetry data to the console. Data is printed in a csv format.
    Columns are fixed width. Three points of decimal precision are used.
    """
    print(f"ts: {time():6.3f}, "
          f"rf_us_d: {right_front_ultrasonic_distance():6.3f} m, "
          f"rb_us_d: {right_back_ultrasonic_distance():6.3f} m, "
          f"l_us_d{left_ultrasonic_distance():6.3f} m, "
          f"f_us_d: {front_ultrasonic_distance():6.3f} m, "
          f"gyro: {math.degrees(gyro_angle()):6.3f} deg, "
          f"mag: {magnetic_reading():4.2f}, "
          f"ir: {ir_reading():4.2f}, "
          f"ir_avg: {0.5 * (grovepi.analogRead(IR_LEFT_PORT) + grovepi.analogRead(IR_RIGHT_PORT)):4}")
