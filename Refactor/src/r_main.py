import pygame
import os
import json

import sys
sys.path.append('../data')
sys.path.append('.')

from r_board import Board
from r_validation import Validator
from gui import GUI
from r_solve import Solver


MAPNUM = 18
ARCHIVE = False
COLOR_PALETTE = "VIBRANT"

def get_original_board_data(mapNum: int):
    
    key = f"map{mapNum}"
    script_dir = os.path.dirname(os.path.abspath(__file__))  
    maps_file = os.path.join(script_dir, '../data/maps.json')
    
    if mapNum not in range(1,101):
        print(f"Invalid Map Number for {maps_file}")
        return None

    with open(maps_file, "r") as file:
        data = json.load(file)
        
    mapData = data[key]
    
    return Board(mapData['name'], mapData['caseNumber'], mapData['colorGrid'])

def get_archive_board_data(mapNum: int):

    script_dir = os.path.dirname(os.path.abspath(__file__))  
    maps_file = os.path.join(script_dir, '../data/archivedqueens.json')

    try:
        with open(maps_file, "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        raise FileNotFoundError(f"The file {maps_file} was not found.")
    except json.JSONDecodeError:
        raise ValueError("Error decoding the JSON file.")
        
    
    formatted_dict = {entry['id']: entry for entry in data}
    
    if mapNum not in formatted_dict:
        raise ValueError(f"Map {mapNum} not found in the dataset.") 

    mapData = formatted_dict[mapNum]
    
    name = f"Map No {mapData['id']}"# - {mapData['date']}"
    size = len(mapData['grid'][0])
    region_map = mapData['regions']
    
    return Board(name, size, region_map)

def load_board(board_data: Board, gui: GUI):
    gui.update_window_size(board_data.size)

def main():
    # MAPNUM =   # Or change to your desired map number
    if ARCHIVE:
        board_data = get_archive_board_data(MAPNUM)
    else:
        board_data = get_original_board_data(MAPNUM)
        
    assert board_data, "BOARD DATA COULD NOT BE LOADED"
    validator = Validator()
    solver = Solver()
    # deducer = Deducer()

    gui = GUI(grid_size=board_data.size, cell_size=60,color_palette_name=COLOR_PALETTE)
    load_board(board_data, gui)
    pygame.display.set_caption(f"Queen's Game - {board_data.name}")

    print(f"{board_data.name}")
    win = False
    running = True
    while running:
        gui.draw(board_data, win)
        running, win = gui.handle_events(board_data, validator,solver,win)

        # Handle additional game logic like deductions, solving, etc.
        if not running:
            break

        # Your additional logic for solving, deduction, etc.
        # Example: Deduction, Brute force solving, etc.

    pygame.quit()

if __name__ == "__main__":
    main()
