from dataclasses import dataclass

from robot_io import io

@dataclass
class MazeMapCell:
    
    

class Maze_map:
    def __init__(self):
        maze_map = []
        x_min = 0
        x_max = 0

        y_min = 0
        y_max = 0


    for i in range(50):
        for j in range(50):
            maze_map.append([0,0,0,0,0,0])

        #Maze_map_cell: 
        # [Path gears took,
        # Not part of path,
        # Origin (starting point of GEARS), 
        # Heat Source,
        # Magnetic Source,
        # Exit Point]


        maze_map_cell = []

        path = 0
        not_part_of_path = 0
        origin = 0
        heat_source = 0
        magentic_source = 0
        exit = 0


        #Maze map contains maze_map_cells

        # Team: 40
        # Map: 0
        # Unit Length: 40
        # Unit: cm
        # Origin: (0,0)



        def print(maze_map):
            for i in range(len(maze_map)):
                for j in range(len(maze_map[i])):
                    print(str(maze_map[i,j]) + " ")

     def update(maze_cell):
        