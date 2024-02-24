"""
The interface to the real robot's sensors and motors.
"""

import math
import time as _time # Avoid name conflict with time module

import brickpi3
import grovepi
from MPU9250 import MPU9250 # IMU library

import constants

# Initialize BrickPi3 and MPU9250 libraries
BP = brickpi3.BrickPi3()
mpu9250 = MPU9250()

# LEGO Sensor Ports
GYRO_PORT = BP.PORT_1
FRONT_ULTRASONIC_PORT = BP.PORT_4

# GrovePi Sensor Ports
LEFT_FRONT_ULTRASONIC_PORT = 3
LEFT_BACK_ULTRASONIC_PORT = 4
IR_LEFT_PORT = 14 # These are for port A0
IR_RIGHT_PORT = 15

# LEGO Motor Ports
DRIVE_LEFT_PORT = BP.PORT_B
DRIVE_RIGHT_PORT = BP.PORT_C
RAMP_PORT = BP.PORT_A

# Keep track of timestamp robot starts at
_initial_time = 0.0

def initialize_io():
    """
    Initializes the LEGO sensors and motors and GrovePi sensors
    """
    # Initialize LEGO sensors
    BP.set_sensor_type(GYRO_PORT, BP.EV3_GYRO_ABS_DPS)
    BP.set_sensor_type(FRONT_ULTRASONIC_PORT, BP.SENSOR_TYPE.EV3_ULTRASONIC_CM)

    # Reset motor encoders
    BP.offset_motor_encoder(
            DRIVE_LEFT_PORT, BP.get_motor_encoder(DRIVE_LEFT_PORT))
    BP.offset_motor_encoder(
            DRIVE_RIGHT_PORT, BP.get_motor_encoder(DRIVE_RIGHT_PORT))

    global _initial_time # Python requires this to modify global variable
    # Initialize timestamp so that time() returns 0 at the start of the program
    _initial_time = _time.time()

def shutdown_io():
    """
    Shuts down the LEGO sensors and motors and GrovePi sensors
    """
    # Kill all motors and sensors
    BP.reset_all()

def left_front_ultrasonic_distance() -> float:
    """
    Returns the distance in meters from the left front ultrasonic sensor
    """
    return BP.ultrasonicRead(LEFT_FRONT_ULTRASONIC_PORT) / 100 # cm -> m

def left_back_ultrasonic_distance() -> float:
    """
    Returns the distance in meters from the left back ultrasonic sensor
    """
    return BP.ultrasonicRead(LEFT_BACK_ULTRASONIC_PORT) / 100 # cm -> m

def front_ultrasonic_distance() -> float:
    """
    Returns the distance in meters from the front ultrasonic sensor
    """
    return BP.get_sensor(FRONT_ULTRASONIC_PORT) / 100 # cm -> m

def gyro_angle() -> bool:
    """
    Returns the heading of the robot from the gyro, in radians
    """
    # Keep iterating until no error happens
    while True:
        try:
            # Get the gyro angle from pair of (angle, rate)
            # Convert to radians, use counter-clockwise as positive
            return -math.radians(BP.get_sensor(GYRO_PORT)[0])
        except brickpi3.SensorError as error:
            print(f"EV3 Gyro error: {error}")

# Cache previous magnet reading
_previous_magnet_reading = 0

def magnetic_obstacle_detected() -> bool:
    """
    Check if a magnetic obstacle is in front of the robot
    """
    global _previous_magnet_reading
    new_magnet_reading = math.sqrt(mpu9250.readMagnet()["x"]**2
                                 + mpu9250.readMagnet()["y"]**2
                                 + mpu9250.readMagnet()["z"]**2)
    if new_magnet_reading != 0:
        _previous_magnet_reading = new_magnet_reading

    return _previous_magnet_reading >= 600

def ir_obstacle_detected() -> bool:
    """
    Check if an IR obstacle is in front of the robot
    """
    avg_ir = 0.5 * (grovepi.analogRead(IR_LEFT_PORT)
                  + grovepi.analogRead(IR_RIGHT_PORT))
    return avg_ir >= 30

def time() -> float:
    return _time.time() - _initial_time

# OUTPUTS
def set_drive_left_speed(wheel_tangential_velocity: float):
    """
    Sets the tangential velocity of the left wheel
    """
    wheel_angular_speed = wheel_tangential_velocity / (
            constants.WHEEL_DIAMETER / 2)
    BP.set_motor_dps(DRIVE_LEFT_PORT,
                     -math.degrees(wheel_angular_speed)
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