# Integrated Codebase

This code is used for all the POC tasks and the final demo.

## IO Abstraction

IO functionality is abstracted and contained to one file: `robot_io.py`. This
provides three benefits:

1. Allows simulation io
2. Keeps all IO errors and issues contained in one file
3. Unit conversions can be done in one place

By replacing each function in `robot_io.py` with a simulated equivalent, you
can get full robot functionality on your computer for testing rather than
just on the robot, which is nice for testing new features and debugging. If
there's ever an issue with IO, you know which file to look in. You can also
tell the robot to move in `m/s` instead of in `deg/s` of the motors, which
makes it easy to command the robot to do something in the real world.

## States and Commands

To model complex robot behaviors, states and commands are used. They execute
functions on the robot like driving and sensing things, using the `execute()`
function which runs repeatedly every ~2 ms.

### States

The robot is always in exactly one state at any given time. After running each
`execute()` function, the next state is returned, which can be either

* the current state
* another state

States are useful for modeling behavior that changes based on outside
influences such as a sensor reading.

### Commands

Commands can be run within the current state. Commands run for however long
their `execute()` function returns `True`. Commands are useful for preplanned
behavior.
