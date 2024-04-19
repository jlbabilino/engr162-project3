# from robot import Robot

# import states.idle_state as idle_state
# import commands.detect_surroundings_command as dsc
# import commands.sequential_command as sc

# class DetectDecideState:
#     def __init__(self, robot: Robot):
#         self.robot = robot

#         self.command = sc.SequentialCommand([
#             dsc.DetectSurroundingsCommand(self.robot),
#             ])

#     def execute(self):
#         direction, checkBeforeApproach = self.robot.maze_map.optimal_next_move()
#         if direction is None:
#             print("No optimal next move found")
#             return idle_state.IdleState()
        
#         print("NavigateMazeState: Optimal next move is", direction)

#         if checkBeforeApproach:

#         return self