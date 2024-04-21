
import constants
from robot import Robot
from robot_io import io

import commands.drive_forward_command as dfc
import commands.sequential_command as sc
import states.command_then_state_state as cts
import states.detect_surroundings_state as dss
import commands.lambda_command as lc

class AttemptDriveNextCell:
    def __init__(self, robot: Robot):
        self.robot = robot

        self.target_int_angle = None

        self.drive_command = None

        self.target_maze_coords = None

    def execute(self):
        if self.target_int_angle == None:
            self.target_int_angle = self.robot.get_heading_int_angle()

            self.drive_command = dfc.DriveForwardCommand(self.robot,
                                                     self.target_int_angle.to_angle(),
                                                     constants.WALL_DISTANCE)
            
            self.target_maze_coords = self.robot.coords.move(self.target_int_angle.to_cardinal_direction())

            self.drive_command.initialize()

        ir_reading = abs(io.ir_reading())
        mag_reading = abs(io.magnetic_reading())

        if ir_reading > constants.IR_THRESHOLD:
            print("IR sensor detected, reversing...")
            self.robot.maze_map.update_ir_hazard(self.target_maze_coords.x,
                                                 self.target_maze_coords.y,
                                                 ir_reading)
            dist_so_far = self.drive_command.distance_traveled()
            reverse_drive_command = dfc.DriveForwardCommand(self.robot,
                                                            self.target_int_angle.to_angle(),
                                                            -dist_so_far)
            return cts.CommandThenStateState(reverse_drive_command,
                                             dss.DetectSurroundingsState(self.robot))
        
        if mag_reading > constants.MAG_THRESHOLD:
            print("Magnet detected, reversing...")
            self.robot.maze_map.update_mag_hazard(self.target_maze_coords.x,
                                                  self.target_maze_coords.y,
                                                  mag_reading)
            dist_so_far = self.drive_command.distance_traveled()
            reverse_drive_command = dfc.DriveForwardCommand(self.robot,
                                                            self.target_int_angle.to_angle(),
                                                            -dist_so_far)
            return cts.CommandThenStateState(reverse_drive_command,
                                             dss.DetectSurroundingsState(self.robot))

        if self.drive_command.execute():
            return cts.CommandThenStateState(
                sc.SequentialCommand([
                    lc.LambdaCommand(
                        lambda: self.robot.maze_map.update_visited_cell(
                            self.target_maze_coords.x,
                            self.target_maze_coords.y)),
                    lc.LambdaCommand(lambda: self.robot.move_maze_coords(self.target_int_angle.to_cardinal_direction()))
                ]),
                dss.DetectSurroundingsState(self.robot))

        return self
