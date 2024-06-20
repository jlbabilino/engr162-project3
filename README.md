# ENGR 162 Team 40 Project 3 2024

Our code for Project 3 of the Purdue University ENGR 162 course. We have been
tasked with designing a robot that can navigate a maze autonomously.

## Changing between Simulation and Real

This codebase can be used to simulate the robot or to run the actual robot.
To set the mode, go to `src/main/robot_io.py`, and make sure only the correct
line is uncommented. If you want simulation, `import sim.sim_robot_io as io`
should be uncommented, and if you want to run on the real robot,
`import real.real_robot_io as io` should be uncommented.

## Running Simulation

The simulation can be run on any computer with a display, and it requires
Matplotlib.

## Running

To run the demo code

```console
cd src/main
python3 run_demo.py
```

<img width="632" alt="simulation visualization window" src="https://github.com/jlbabilino/engr162-project3/assets/28580376/e8fffee5-92ff-439f-bbef-9acd5abcddde">
