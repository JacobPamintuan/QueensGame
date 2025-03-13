import unittest

import sys
import os

# Add the 'src' directory to the system path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Refactor/src')))

# Now you should be able to import your modules from 'src'
from r_board import Board
from r_validation import Validator
from r_solve import Solver
# from r_deduce import Deducer

import time
import json

# Path to the JSON file
MAPS_FILE = "maps_data/maps.json"



    
def get_board_data_original(maps_file, mapNum: int):
    key = f"map{mapNum}"

    maps_file = r"maps_data\maps.json"

    
    with open(maps_file, "r") as file:
        data = json.load(file)
        
    mapData = data[key]
    
    return Board(mapData['name'], mapData['caseNumber'], mapData['colorGrid'])
    
    return Board(name, size, region_map)
def internal_BFOS(board: Board, solver: Solver, validator: Validator):
    """Runs internal deduction and brute force with optimal seed."""

    # deducer.reduce_board_state(board)
    solver.brute_force_optimal_seed(board)
    return validator.validate_win(board)
    
    # return validator.validate_win(board)



class TestAlgorithmIDBFOS(unittest.TestCase):
    
    def _test_algorithm_IDBFOS(self, mapNum):
        """Test Internal Deduction -> Brute Force Optimal Seed on a single map."""
        board = get_board_data_original(MAPS_FILE, mapNum)
        validator = Validator()
        solver = Solver()
        # deducer = Deducer()

        # start_time = time.time()
        # final_board = internal_deduce_BFOS(board, deducer, solver)
        # elapsed_time = time.time() - start_time

        # solved = validator.validate_win(final_board)
        
        start_time = time.time()
        solved = internal_BFOS(board, solver, validator)
        elapsed_time = time.time() - start_time

        

        self.assertTrue(solved, f"Algorithm BFOS failed on Map {mapNum} (Time: {elapsed_time:.4f}s)")

# Dynamically create test methods for each map ID
def create_dynamic_tests():
    for mapNum in range(1,101):
        def test_method(self, mapNum=mapNum):
            """Dynamically created test method."""
            self._test_algorithm_IDBFOS(mapNum)
        
        # Add a `test_` prefix to the method name
        test_method_name = f'test_OG_map_{mapNum}'
        setattr(TestAlgorithmIDBFOS, test_method_name, test_method)

# Create dynamic test methods
create_dynamic_tests()
# class TestAlgorithmIDBFOS(unittest.TestCase):
    
#     def _test_algorithm_IDBFOS(self, mapNum):
#         """Test Internal Deduction -> Brute Force Optimal Seed on a single map."""
#         board = get_board_data_archive(MAPS_FILE, mapNum)
#         validator = Validator()
#         solver = Solver(validator)
#         deducer = Deducer()

#         start_time = time.time()
#         final_board = internal_deduce_BFOS(board, deducer, solver)
#         elapsed_time = time.time() - start_time

#         solved = validator.validate_win(final_board)

#         self.assertTrue(solved, f"Algorithm BFOS failed on Map {mapNum} (Time: {elapsed_time:.4f}s)")

# # Dynamically create test methods for each map ID
# for mapNum in MAP_IDS:
#     # Define a new test method for each mapNum and set its name dynamically
#     test_method_name = f'test_map_{mapNum}'#_algorithm_IDBFOS'
#     # Use setattr to add the method to the TestAlgorithmIDBFOS class
#     setattr(TestAlgorithmIDBFOS, test_method_name, lambda self, mapNum=mapNum: self._test_algorithm_IDBFOS(mapNum))

if __name__ == "__main__":
    unittest.main()
