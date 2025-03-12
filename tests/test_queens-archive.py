import time
import json
import unittest
from src.board import Board
from src.validate import Validator
from src.solve import Solver
from src.deduce import Deducer

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

def internal_deduce_BFOS(board: Board, deducer: Deducer, solver: Solver):
    """Runs internal deduction and brute force with optimal seed."""

    deducer.reduce_board_state(board)
    return solver.brute_force_optimal_seed(board)

# Load map IDs dynamically from the JSON file
MAP_IDS = load_map_ids(MAPS_FILE)

class TestAlgorithmIDBFOS(unittest.TestCase):
    
    def _test_algorithm_IDBFOS(self, mapNum):
        """Test Internal Deduction -> Brute Force Optimal Seed on a single map."""
        board = get_board_data_archive(MAPS_FILE, mapNum)
        validator = Validator()
        solver = Solver(validator)
        deducer = Deducer()

        start_time = time.time()
        final_board = internal_deduce_BFOS(board, deducer, solver)
        elapsed_time = time.time() - start_time

        solved = validator.validate_win(final_board)

        self.assertTrue(solved, f"Algorithm BFOS failed on Map {mapNum} (Time: {elapsed_time:.4f}s)")

# Dynamically create test methods for each map ID
for mapNum in MAP_IDS:
    # Define a new test method for each mapNum and set its name dynamically
    test_method_name = f'test_map_{mapNum}'#_algorithm_IDBFOS'
    # Use setattr to add the method to the TestAlgorithmIDBFOS class
    setattr(TestAlgorithmIDBFOS, test_method_name, lambda self, mapNum=mapNum: self._test_algorithm_IDBFOS(mapNum))

if __name__ == "__main__":
    unittest.main()
