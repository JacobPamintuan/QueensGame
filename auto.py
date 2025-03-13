import os
import sys
import time
import json
import csv

# Correcting paths to point inside QueensGame/
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'Refactor', 'src')))

# Debugging: Check if paths are correct
print("Updated sys.path:")
for p in sys.path:
    print(p)

from src.solve import Solver as Solver_SRC
from Refactor.src.r_solve import Solver as Solver_Refactor
from src.board import Board
from src.validate import Validator
from src.deduce import Deducer
from Refactor.src.r_board import Board as Board_Refactor
from Refactor.src.r_validation import Validator as Validator_Refactor


# Function to get board data (same as the previous code, for testing)
def get_board_data_src(mapNum: int):
    key = f"map{mapNum}"

    maps_file = r"Refactor\data\maps.json"
    
    with open(maps_file, "r") as file:
        data = json.load(file)
    
    mapData = data[key]
    
    return Board(mapData['name'], mapData['caseNumber'], mapData['colorGrid'])

def get_board_data_refactor(mapNum: int):
    key = f"map{mapNum}"

    maps_file = r"Refactor\data\maps.json"
    
    with open(maps_file, "r") as file:
        data = json.load(file)
    
    mapData = data[key]
    
    return Board_Refactor(mapData['name'], mapData['caseNumber'], mapData['colorGrid'])

# Run BFOS from both versions of Solver
def run_bfos_test(mapNum: int, 
                  board_src: Board, board_refactor : Board_Refactor, 
                  solver_src: Solver_SRC, solver_refactor: Solver_Refactor, 
                  validator_src: Validator, validator_refactor : Validator_Refactor,
                  deducer: Deducer):
    print(f"Running BFOS on Map #{mapNum}")

    # Timing and executing the BFOS algorithm from the 'src' version
    start_time = time.time()
    final_board_src = solver_src.brute_force_optimal_seed(board_src)
    elapsed_src = time.time() - start_time
    solved_src = validator_src.validate_win(final_board_src)
    num_seeds_src = solver_src.num_seeds
    chosen_seed_src = solver_src.chosen_seed
    print(f"src BFOS Time: {elapsed_src:.6f}s, Solved: {solved_src}, Seeds Attempted: {num_seeds_src}, Chosen Seed: {chosen_seed_src}")

    # Timing and executing the BFOS algorithm from the 'Refactor/src' version
    start_time = time.time()
    final_board_refactor = solver_refactor.brute_force_optimal_seed(board_refactor, None)
    elapsed_refactor = time.time() - start_time
    solved_refactor = validator_refactor.validate_win(board_refactor)
    num_seeds_refactor = solver_refactor.num_seeds
    chosen_seed_refactor = solver_refactor.chosen_seed
    print(f"Refactor/src BFOS Time: {elapsed_refactor:.6f}s, Solved: {solved_refactor}, Seeds Attempted: {num_seeds_refactor}, Chosen Seed: {chosen_seed_refactor}")

    # Check if the chosen seeds are the same
    chosen_seed_same = chosen_seed_src == chosen_seed_refactor

    return {
        "mapNum": mapNum,
        "src_time": elapsed_src,
        "refactor_time": elapsed_refactor,
        "src_solved": solved_src,
        "refactor_solved": solved_refactor,
        "src_seeds": num_seeds_src,
        "refactor_seeds": num_seeds_refactor,
        "src_chosen_seed": chosen_seed_src,
        "refactor_chosen_seed": chosen_seed_refactor,
        "chosen_seed_same": chosen_seed_same  # New key to track if seeds are the same
    }

# Write the results to a CSV file
def write_results_to_csv(results, filename="autotest_results.csv"):
    with open(filename, mode="w", newline="") as file:
        writer = csv.writer(file)
        header = [
            "Map", 
            "src Time (s)", "Refactor/src Time (s)", 
            "src Solved", "Refactor/src Solved", 
            "src Seeds Attempted", "Refactor/src Seeds Attempted", 
            "src Chosen Seed", "Refactor/src Chosen Seed",
            "Chosen Seed Same"  # New column for seed comparison
        ]
        writer.writerow(header)
        for result in results:
            writer.writerow([ 
                result["mapNum"], 
                result["src_time"], result["refactor_time"], 
                result["src_solved"], result["refactor_solved"], 
                result["src_seeds"], result["refactor_seeds"], 
                result["src_chosen_seed"], result["refactor_chosen_seed"],
                result["chosen_seed_same"]  # Write the value for the seed comparison
            ])
    print(f"Results saved to {filename}")

def main():
    # Define the range of maps to test
    results = []
    for mapNum in range(1, 101):  # Change this to 1, 101 for full range
        # Get board data for the current map
        board_src = get_board_data_src(mapNum)
        board_refactor = get_board_data_refactor(mapNum)
        
        validator_src = Validator()
        validator_refactor = Validator_Refactor()

        deducer_src = Deducer()

        # Create solver instances for both src and refactor/src
        solver_src = Solver_SRC(validator_src)
        solver_refactor = Solver_Refactor()

        # Run BFOS on both versions
        result = run_bfos_test(mapNum, board_src, board_refactor, solver_src, solver_refactor, validator_src, validator_refactor, deducer_src)
        results.append(result)

        filename = r"autotest_results.csv"

        try:
            write_results_to_csv(results)
        except PermissionError:
            print(f"Warning: Could not save file {filename}. The file might be open. Skipping save...")


    # Write results to CSV
    write_results_to_csv(results)

if __name__ == "__main__":
    main()
