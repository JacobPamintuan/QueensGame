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

# Testing Internal_overlap: 287
# Testing row_col_overlap: 179, 203, 180, 269

MAPNUM = 323
ARCHIVE = True
COLOR_PALETTE = "VIBRANT"

MAPS_FILE_ORIGINAL = "data/maps.json"
MAPS_FILE_ARCHIVE = "data/archivedqueens.json"

def update_archive():
    try:
        req = requests.get("https://queensstorage.blob.core.windows.net/puzzles/linkedinPuzzles.json")
        
        data = req.json()
        
        
        
    
        formatted_dict = {entry['id']: entry for entry in data}
        
        formatted_dict[177]['regions'][6][7] = 9
        formatted_dict[177]['regions'][6][8] = 9
        formatted_dict[177]['regions'][7][7] = 9
        formatted_dict[177]['regions'][7][8] = 9
        
        # script_dir = os.path.dirname(os.path.abspath(__file__))  
        # # maps_file = os.path.join(script_dir, '../data/archivedqueens.json')
        # maps_file = os.path.join(script_dir, '../../maps_data/archivedqueens.json')
        # # maps_file = os.path.join(script_dir, '../../maps_data/test.json')
        
        with open(MAPS_FILE_ARCHIVE, 'w') as file:
            json.dump(list(formatted_dict.values()), file, indent=4)
            
        print("ARCHIVE UPDATED")
    except requests.exceptions.RequestException as e:
        # Issues with the GET request
        print(f"Request failed: {e}")
        return False

    except FileNotFoundError as e:
        # File path doesn't exist
        print(f"File not found: {e}")
        return False

    except Exception as e:
        # General exception handler 
        print(f"An unexpected error occurred: {e}")
        return False
    
    return True
    

def get_original_board_data(mapNum: int):
    
    key = f"map{mapNum}"

    
    if mapNum not in range(1,101):
        print(f"Invalid Map Number for {MAPS_FILE_ORIGINAL}")
        return None

    with open(MAPS_FILE_ORIGINAL, "r") as file:
        data = json.load(file)
        
    mapData = data[key]
    
    return Board(mapData['name'], mapData['caseNumber'], mapData['colorGrid'])

def get_archive_board_data(mapNum: int):

    try:
        with open(MAPS_FILE_ARCHIVE, "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        raise FileNotFoundError(f"The file {MAPS_FILE_ARCHIVE} was not found.")
    except json.JSONDecodeError:
        raise ValueError("Error decoding the JSON file.")
        
    
    formatted_dict = {entry['id']: entry for entry in data}
    
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

    if ARCHIVE:
        update_archive()
        board_data = get_archive_board_data(MAPNUM)
    else:
        board_data = get_original_board_data(MAPNUM)
        
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
