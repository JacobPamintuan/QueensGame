import pygame
import os
import json

import sys
sys.path.append('../data')
sys.path.append('.')

from r_board import Board
from r_validation import Validator
from gui import GUI


MAPNUM = 1
COLOR_PALETTE = "VIBRANT"

def get_board_data(mapNum: int):
    key = f"map{mapNum}"
    script_dir = os.path.dirname(os.path.abspath(__file__))  
    maps_file = os.path.join(script_dir, '../data/maps.json')

    with open(maps_file, "r") as file:
        data = json.load(file)
        
    mapData = data[key]
    
    return Board(mapData['name'], mapData['caseNumber'], mapData['colorGrid'])

def load_board(board_data: Board, gui: GUI):
    gui.update_window_size(board_data.size)

def main():
    MAPNUM = 84  # Or change to your desired map number
    board_data = get_board_data(MAPNUM)
    validator = Validator()
    # solver = Solver(validator)
    # deducer = Deducer()

    gui = GUI(grid_size=board_data.size, cell_size=60,color_palette_name=COLOR_PALETTE)
    load_board(board_data, gui)
    pygame.display.set_caption(f"Queen's Game - {board_data.name}")

    print(f"{board_data.name}")
    win = False
    running = True
    while running:
        gui.draw(board_data, win)
        running, win = gui.handle_events(board_data, validator,win)

        # Handle additional game logic like deductions, solving, etc.
        if not running:
            break

        # Your additional logic for solving, deduction, etc.
        # Example: Deduction, Brute force solving, etc.

    pygame.quit()

if __name__ == "__main__":
    main()
