import unittest
import sys
import os
import time
import json

# Add the 'src' directory to the system path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

# Import necessary modules
from board import Board
from validate import Validator
from solve import Solver
from deduce import Deducer

# Paths to JSON files
MAPS_FILE_ORIGINAL = "maps_data/maps.json"
MAPS_FILE_ARCHIVE = "maps_data/archivedqueens.json"

def load_map_ids(maps_file):
    """Loads all map IDs from the JSON file dynamically."""
    with open(maps_file, "r") as file:
        data = json.load(file)  # Load JSON list
    
    return [entry['id'] for entry in data]  # Extract all map IDs

def get_board_data(maps_file, mapNum: int, is_archive=False):
    """Retrieves board data for a given mapNum from the JSON file."""
    with open(maps_file, "r") as file:
        data = json.load(file)
    
    if is_archive:
        formatted_dict = {entry['id']: entry for entry in data}
        if mapNum not in formatted_dict:
            raise ValueError(f"Map {mapNum} not found in {maps_file}")
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

def deduce_BFOS(board: Board, deducer: Deducer, solver: Solver, validator: Validator):
    """Runs internal deduction and brute force with optimal seed."""
    deducer.reduce_board_state(board)
    return solver.brute_force_optimal_seed(board)

class TestOriginal(unittest.TestCase):
    """Tests for the original dataset."""
    
    def _test_OG(self, mapNum):
        board = get_board_data(MAPS_FILE_ORIGINAL, mapNum)
        validator = Validator()
        solver = Solver(validator)
        deducer = Deducer()
        
        start_time = time.time()
        solved = deduce_BFOS(board, deducer, solver, validator)
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
        board = get_board_data(MAPS_FILE_ARCHIVE, mapNum, is_archive=True)
        validator = Validator()
        solver = Solver(validator)
        deducer = Deducer()
        
        start_time = time.time()
        solved = deduce_BFOS(board, deducer, solver, validator)
        elapsed_time = time.time() - start_time
        
        self.assertTrue(solved, f"Algorithm BFOS failed on Map {mapNum} (Time: {elapsed_time:.4f}s)")

# Load map IDs dynamically for the archived dataset
MAP_IDS = load_map_ids(MAPS_FILE_ARCHIVE)
for mapNum in MAP_IDS:
    def test_method(self, mapNum=mapNum):
        self._test_ARCH(mapNum)
    setattr(TestArchive, f'test_ARCH_map_{mapNum}', test_method)

if __name__ == "__main__":
    unittest.main()
