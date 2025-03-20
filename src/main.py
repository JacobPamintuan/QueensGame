import pygame
import os
import json
import requests

# import sys


from board import Board
from validation import Validator
from gui import GUI
from solve import Solver
from deduce import Deducer
from update_maps import MapData

# Testing Internal_overlap: 287
# Testing row_col_overlap: 179, 203, 180, 269

MAPNUM = -1
ARCHIVE = True
COLOR_PALETTE = "VIBRANT"

MAPS_FILE_ORIGINAL = "data/maps.json"
MAPS_FILE_ARCHIVE = "data/archivedqueens.json"


def get_original_board_data(data, mapNum):
    
    key = f"map{mapNum}"

    
    if mapNum not in range(1,101):
        print(f"Invalid Map Number for {MAPS_FILE_ORIGINAL}")
        return None

    mapData = data[key]
    
    return Board(mapData['name'], mapData['caseNumber'], mapData['colorGrid'])

def get_archive_board_data(data, mapNum: int):

    
    formatted_dict = {entry['id']: entry for entry in data}
    
    if mapNum == -1:
        mapNum = max(formatted_dict.keys())

    if mapNum not in formatted_dict:
        raise ValueError(f"Map {mapNum} not found in the dataset.") 

    mapData = formatted_dict[mapNum]

    name = f"Map No {mapData['id']}"
    
    date = mapData.get('date', None)
    if date:
        name = f"Map {mapData['id']} - {mapData['date']}"

    size = len(mapData['grid'][0])
    region_map = mapData['regions']
    
    return Board(name, size, region_map)

def load_board(board_data: Board, gui: GUI):
    gui.update_window_size(board_data.size)

def main():

    map_data = MapData(ARCHIVE)
    
    assert map_data, "MAP DATA COULD NOT BE LOADED"
    

    if ARCHIVE:
        board_data = get_archive_board_data(map_data.data, MAPNUM)
    else:
        board_data = get_original_board_data(map_data.data, MAPNUM)
        
    assert board_data, "BOARD DATA COULD NOT BE LOADED"
    validator = Validator()
    solver = Solver()
    deducer = Deducer()

    caption = f"Queen's Game: {board_data.name}"
    gui = GUI(caption, grid_size=board_data.size, cell_size=60,color_palette_name=COLOR_PALETTE)
    load_board(board_data, gui)


    print(f"{board_data.name}")
    win = False
    running = True
    while running:
        gui.draw(board_data, win)
        running, win = gui.handle_events(board_data, validator,solver,deducer, win)

        # Handle additional game logic like deductions, solving, etc.
        if not running:
            break


    pygame.quit()

if __name__ == "__main__":
    main()
