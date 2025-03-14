import unittest

import sys
import os

# Add the 'src' directory to the system path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Refactor/src')))


# Now you should be able to import your modules from 'src'
from r_board import Board
from r_validation import Validator
from r_solve import Solver
from r_deduce import Deducer

import time
import json

# Path to the JSON file
MAPS_FILE = "maps_data/archivedqueens.json"

def load_map_ids(maps_file):
    """Loads all map IDs from the JSON file dynamically."""
    with open(maps_file, "r") as file:
        data = json.load(file)  # Load JSON list
    
    return [entry['id'] for entry in data]  # Extract all map IDs

def get_board_data_archive(maps_file, mapNum: int):
    """Retrieves board data for a given mapNum from the JSON file."""
    with open(maps_file, "r") as file:
        data = json.load(file)

    formatted_dict = {entry['id']: entry for entry in data}

    if mapNum not in formatted_dict:
        raise ValueError(f"Map {mapNum} not found in {maps_file}")

    mapData = formatted_dict[mapNum]
    
    name = f"Map No {mapData['id']}"# - {mapData['date']}"

    size = len(mapData['grid'])
    region_map = mapData['regions']
    
    return Board(name, size, region_map)

def full_deduction(board: Board, deducer: Deducer, solver: Solver, validator: Validator):

    deducer.full_reduce_board(board)
    # return solver.brute_force_optimal_seed(board)
    return validator.validate_win(board)


# Load map IDs dynamically from the JSON file
MAP_IDS = load_map_ids(MAPS_FILE)
class TestAlgorithmIDBFOS(unittest.TestCase):
    
    def _test_algorithm_IDBFOS(self, mapNum):
        """Test Internal Deduction -> Brute Force Optimal Seed on a single map."""
        board = get_board_data_archive(MAPS_FILE, mapNum)
        validator = Validator()
        solver = Solver()
        deducer = Deducer()

        # start_time = time.time()
        # final_board = internal_deduce_BFOS(board, deducer, solver)
        # elapsed_time = time.time() - start_time

        # solved = validator.validate_win(final_board)
        
        start_time = time.time()
        solved = full_deduction(board, deducer, solver, validator)
        elapsed_time = time.time() - start_time

        

        self.assertTrue(solved, f"Algorithm BFOS failed on Map {mapNum} (Time: {elapsed_time:.4f}s)")

# Dynamically create test methods for each map ID
def create_dynamic_tests():
    for mapNum in MAP_IDS:
        def test_method(self, mapNum=mapNum):
            """Dynamically created test method."""
            self._test_algorithm_IDBFOS(mapNum)
        
        # Add a `test_` prefix to the method name
        test_method_name = f'test_map_{mapNum}'
        setattr(TestAlgorithmIDBFOS, test_method_name, test_method)

# Create dynamic test methods
create_dynamic_tests()


if __name__ == "__main__":
    unittest.main()
