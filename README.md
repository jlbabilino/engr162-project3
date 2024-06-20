# ENGR 162 Team 40 Project 3, Spring 2024

Our robot code for Project 3 of the Purdue University ENGR 162 course. We were
tasked with designing a robot that could navigate a maze autonomously. Our robot
successfully completed the demonstration course entirely on its own using ultrasonic
sensors to navigate through a maze. Created by engineering students Justin Babilino,
Isabella Levine, Ellie Dunlevy, and Nick Savage.

## Changing between Simulation and Real

This codebase can be used to simulate the robot or to run the actual robot.
To set the mode, go to `src/main/robot_io.py`, and make sure only the correct
line is uncommented. If you want simulation, `import sim.sim_robot_io as io`
should be uncommented, and if you want to run on the real robot,
`import real.real_robot_io as io` should be uncommented.

## Running Simulation

The simulation can be run on any computer with a display, and it requires
[Matplotlib](https://pypi.org/project/matplotlib/).

## Running

To run the demo code, run the following:

```console
cd src/main
python3 run_demo.py
```

If you get an error message about `brickpi3` not being found, make sure to follow the [above steps](https://github.com/jlbabilino/engr162-project3/edit/main/README.md#changing-between-simulation-and-real) to change to simulation mode.

A Matplotlib window will open showing the robot (blue box 🟦), ultrasonic sensor distances (green lines) walls of maze, IR obstacles (red circles 🔴), and magnetic obstacles (purple circles 🟣):

<img width="632" alt="simulation visualization window" src="https://github.com/jlbabilino/engr162-project3/assets/28580376/e8fffee5-92ff-439f-bbef-9acd5abcddde">

Resulting map printed after solving maze:

```
                                                         
   ⚬   S   X   H   ⚬   ⚬   M   ⚬   ⚬   ⚬   ⚬   ⚬   ⚬   ⚬
                  ─── ───                                
   ⚬   ⚬ │ X   ⚬ │ X   X   X │ ⚬   ⚬   ⚬   ⚬   ⚬   ⚬   ⚬
                      ───                                
   ⚬   ⚬ │ X   X   X │ ⚬   M   ⚬   ⚬   ⚬   ⚬   ⚬   ⚬   ⚬
          ───     ───                                    
   ⚬   ⚬   ⚬ │ X   ⚬   ⚬   ⚬   ⚬   ⚬   ⚬   ⚬   ⚬   ⚬   ⚬
                                                         
   ⚬   ⚬   ⚬ │ X   ⚬   ⚬   ⚬   ⚬   ⚬   ⚬   ⚬   ⚬   ⚬   ⚬
                                                         
   ⚬   ⚬   ⚬ │ X   ⚬   X   X   X   X   X │ ⚬   ⚬   ⚬   ⚬
                          ─── ─── ───                    
   ⚬   ⚬   ⚬ │ X   X   X │ ⚬   ⚬   ⚬ │ X   X   X   X   ⚬
              ─── ─── ───             ─── ─── ─── ───
```

Notice that not all walls are necessarily detected, just enough to make it through the maze.

## Real life robot

Here is a photo of the LEGO robot used during the demonstration:

![4233E79D-2A98-4282-86D0-F1E1341E82EF_1_105_c](https://github.com/jlbabilino/engr162-project3/assets/28580376/de14181f-e280-4fa7-8e96-d747ef163916)

A photo of the robot on the demonstration course, carrying cargo:

<img width="1374" alt="image" src="https://github.com/jlbabilino/engr162-project3/assets/28580376/168fa9e1-c47c-41e6-89e1-9aa75b2dbcd6">
