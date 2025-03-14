import unittest
import sys
import os
import time
import json

# Add the 'src' directory to the system path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Refactor/src')))

# Import necessary modules
from r_board import Board
from r_validation import Validator
from r_solve import Solver
from r_deduce import Deducer
from r_main import update_archive

# Paths to JSON files
MAPS_FILE_ORIGINAL = "maps_data/maps.json"
MAPS_FILE_ARCHIVE = "maps_data/archivedqueens.json"

def load_map_data(maps_file):
    """Loads all map data from the JSON file into memory."""
    with open(maps_file, "r") as file:
        data = json.load(file)
    return data

# Load the map data once at the beginning
original_data = load_map_data(MAPS_FILE_ORIGINAL)
archive_data = load_map_data(MAPS_FILE_ARCHIVE)

def load_map_ids(data):
    """Loads all map IDs from the given data."""
    
    update_archive()
    
    if isinstance(data, list):  # If the data is a list of maps
        return [entry['id'] for entry in data]
    else:  # Assuming the data is a dict for the original dataset
        return list(data.keys())  # Using keys (map IDs)

def get_board_data(data, mapNum: int, is_archive=False):
    """Retrieves board data for a given mapNum from the loaded data."""
    if is_archive:
        formatted_dict = {entry['id']: entry for entry in data}
        if mapNum not in formatted_dict:
            raise ValueError(f"Map {mapNum} not found in archive data")
        mapData = formatted_dict[mapNum]
        name = f"Map No {mapData['id']}"
        size = len(mapData['grid'])
        region_map = mapData['regions']
    else:
        key = f"map{mapNum}"
        mapData = data[key]
        name = mapData['name']
        size = mapData['caseNumber']
        region_map = mapData['colorGrid']
    
    return Board(name, size, region_map)

def deduce_to_BFOS(board: Board, solver: Solver, validator: Validator, deducer: Deducer):
    """Runs internal deduction and brute force with optimal seed."""
    deducer.full_reduce_board(board)
    return solver.brute_force_optimal_seed(board)

def full_deduction(board: Board, deducer: Deducer, solver: Solver, validator: Validator):
    """Runs deduction and validates the solution."""
    deducer.full_reduce_board(board)
    return validator.validate_win(board)

class TestOriginal(unittest.TestCase):
    """Tests for the original dataset."""
    
    def _test_OG(self, mapNum):
        board = get_board_data(original_data, mapNum)
        validator = Validator()
        solver = Solver()
        deducer = Deducer()
        
        start_time = time.time()
        solved = deduce_to_BFOS(board, solver, validator, deducer)
        elapsed_time = time.time() - start_time
        
        self.assertTrue(solved, f"Algorithm BFOS failed on Map {mapNum} (Time: {elapsed_time:.4f}s)")

# Dynamically create test methods for the original dataset
for mapNum in range(1, 101):
    def test_method(self, mapNum=mapNum):
        self._test_OG(mapNum)
    setattr(TestOriginal, f'test_OG_map_{mapNum}', test_method)

class TestArchive(unittest.TestCase):
    """Tests for the archived dataset."""
    
    def _test_ARCH(self, mapNum):
        board = get_board_data(archive_data, mapNum, is_archive=True)
        validator = Validator()
        solver = Solver()
        deducer = Deducer()
        
        start_time = time.time()
        solved = full_deduction(board, deducer, solver, validator)
        elapsed_time = time.time() - start_time
        
        self.assertTrue(solved, f"Algorithm BFOS failed on Map {mapNum} (Time: {elapsed_time:.4f}s)")

# Load map IDs dynamically for the archived dataset
MAP_IDS = load_map_ids(archive_data)
for mapNum in MAP_IDS:
    def test_method(self, mapNum=mapNum):
        self._test_ARCH(mapNum)
    setattr(TestArchive, f'test_ARCH_map_{mapNum}', test_method)

if __name__ == "__main__":
    unittest.main()
