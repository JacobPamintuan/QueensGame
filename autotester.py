from board import Board
from validate import Validator
from solve import Solver
from deduce import Deducer
import copy
import os
import json
import time
import csv
import os

import pygame

class Stats:
    def __init__(self, algo_name, board : Board, elapsed, passed : bool, seeds_attempted : int, chosen_seed : tuple):
        self.algo_name = algo_name
        self.board = copy.deepcopy(board)
        self.elapsed = elapsed
        self.passed = passed
        self.seeds_attempted = seeds_attempted
        self.chosen_seed = chosen_seed


CELL_SIZE = 60
WINDOW_PADDING = 20  # Extra spacing for a cleaner look

def get_board_data(mapNum: int):
    key = f"map{mapNum}"

    script_dir = os.path.dirname(os.path.abspath(__file__))  
    maps_file = os.path.join(script_dir, 'maps.json')

    
    with open(maps_file, "r") as file:
        data = json.load(file)
        
    mapData = data[key]
    
    return Board(mapData['name'], mapData['caseNumber'], mapData['colorGrid'])



def display_boards(map_stats, mapNum, image_folder):
    pygame.init()
    pygame.font.init()

    algo1_stats, algo2_stats = map_stats  # Unpack the tuple
    grid_size = algo1_stats.board.size  # Get board size
    CELL_SIZE = 600 // grid_size  # Adjust cell size dynamically

    WINDOW_SIZE = grid_size * CELL_SIZE
    WINDOW_PADDING = 30  
    screen_width = (WINDOW_SIZE * 2) + WINDOW_PADDING + 10  
    screen_height = WINDOW_SIZE + 200  # Extra height for text display

    screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
    pygame.display.set_caption(f"Comparison - Map {algo1_stats.board.name}")

    screen.fill((255, 255, 255))
    font = pygame.font.Font(None, 24)

    # Compare final board states
    boards_match = algo1_stats.board == algo2_stats.board
    match_text = "Final Boards Match: YES" if boards_match else "Final Boards Match: NO"
    match_color = (0, 150, 0) if boards_match else (200, 0, 0)  # Green for match, red for no match

    # Draw captions above each board
    caption_algo1 = font.render(f"{algo1_stats.algo_name} - {grid_size}x{grid_size}", True, (0, 0, 0))
    caption_algo2 = font.render(f"{algo2_stats.algo_name} - {grid_size}x{grid_size}", True, (0, 0, 0))
    match_text_render = font.render(match_text, True, match_color)

    screen.blit(caption_algo1, (WINDOW_SIZE // 2 - caption_algo1.get_width() // 2, 10))
    screen.blit(caption_algo2, (WINDOW_SIZE + WINDOW_PADDING + (WINDOW_SIZE // 2 - caption_algo2.get_width() // 2), 10))
    screen.blit(match_text_render, (screen_width // 2 - match_text_render.get_width() // 2, screen_height - 40))  # Centered at bottom

    # Draw boards
    algo1_stats.board.draw_board(screen.subsurface((0, 50, WINDOW_SIZE, WINDOW_SIZE)), algo1_stats.passed)
    algo2_stats.board.draw_board(screen.subsurface((WINDOW_SIZE + WINDOW_PADDING, 50, WINDOW_SIZE, WINDOW_SIZE)), algo2_stats.passed)

    # Display additional information
    info_start_y = WINDOW_SIZE + 60
    info_x = 20

    stats = [
        f"Board Size: {grid_size}x{grid_size}",
        f"Algo 1 | Time: {algo1_stats.elapsed:.4f}s | Solved: {algo1_stats.passed} | Seeds: {algo1_stats.seeds_attempted} | Seed: {algo1_stats.chosen_seed}",
        f"Algo 2 | Time: {algo2_stats.elapsed:.4f}s | Solved: {algo2_stats.passed} | Seeds: {algo2_stats.seeds_attempted} | Seed: {algo2_stats.chosen_seed}",
    ]

    for i, stat in enumerate(stats):
        stat_text = font.render(stat, True, (0, 0, 0))
        screen.blit(stat_text, (info_x, info_start_y + (i * 25)))

    pygame.display.flip()

    # Save the image
    image_path = os.path.join(image_folder, f"comparison_Map_{mapNum}.png")
    pygame.image.save(screen, image_path)

    pygame.quit()
    return image_path, boards_match  # Return both the saved image path and whether the boards match



def run_algo(algo_fn, algo_name, mapNum, board : Board, solver : Solver, validator : Validator, deducer=None):
    print("\n-----------------------------------------------------------")
    print(f"MAP #{mapNum}")

    # Timing and executing the brute force algorithm
    print(f"Running {algo_name} algorithm...")

    start_time = time.time()
    final_board = algo_fn(board, deducer, solver)
    end_time = time.time()
    
    elapsed = end_time - start_time  # Time taken for brute_force
    
    print(f"{algo_name} Time: {elapsed:.6f}s")

    is_solved = validator.validate_win(final_board)  # Validation result for brute_force
    print(f"{algo_name} Solved: {is_solved}")

    num_seeds = solver.num_seeds
    print(f"{algo_name} Seeds Attempted: {num_seeds}")

    chosen_seed = solver.chosen_seed
    print(f"{algo_name} Chosen Seed: {chosen_seed}")

    return Stats(algo_name, final_board, elapsed,is_solved,num_seeds,chosen_seed)




def write_to_csv(filename, results, algo1_name, algo2_name):
    """Overwrites the CSV file with all results at once, with dynamic headers."""
    with open(filename, mode="w", newline="") as file:  # "w" mode to overwrite
        writer = csv.writer(file)

        # Dynamically generate the header based on algorithm names
        header = [
            "Map", "Board Size",
            f"{algo1_name} Time (s)", f"{algo1_name} Solved", f"{algo1_name} Seeds", f"{algo1_name} Chosen Seed",
            f"{algo2_name} Time (s)", f"{algo2_name} Solved", f"{algo2_name} Seeds", f"{algo2_name} Chosen Seed",
            "Boards Match", "Image Path"
        ]
        
        writer.writerow(header)  # Write header

        # Write all results from the list
        writer.writerows(results)





def safe_write_to_csv(filename, results, algo_1_name, algo_2_name):
    """Tries to write to the CSV file, prompting the user if the file is open."""
    while True:
        try:
            write_to_csv(filename, results, algo_1_name, algo_2_name)  # Pass algorithm names
            print(f"Results successfully saved to {filename}.")
            break  # Exit loop if successful
        except PermissionError:
            print(f"Error: Could not save {filename}. The file might be open.")
            input("Please close the file and press Enter to retry...")


def format_time(seconds):
    """Formats time into hours, minutes, and seconds."""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = seconds % 60
    return f"{hours}h {minutes}m {seconds:.2f}s"


def internal_deduce_BF(board: Board, deducer: Deducer, solver : Solver):
    deduction = True
    while(deduction):
        deduction = deducer.internal_overlap(board)

    return solver.brute_force(board,None)

def internal_deduce_BFOS(board: Board, deducer: Deducer, solver : Solver):
    deduction = True
    while(deduction):
        deduction = deducer.internal_overlap(board)

    return solver.brute_force_optimal_seed(board,None)

def internal_rowcol_deduce_BFOS(board: Board, deducer: Deducer, solver : Solver):
    deducer.reduce_board_state(board)

    return solver.brute_force_optimal_seed(board,None)
    


# Initialize the dictionary to store map data
map_times = {}

def main():

    image_folder = r"Analysis\Internal_Deduction1"

    os.makedirs(image_folder, exist_ok=True)
    csv_filename = os.path.join(image_folder, "output.csv")


    results = []

    begin_time = time.time()

     # Define the specific maps to test (instead of iterating over all 100)
    for mapNum in range(1,101):  # Maps you want to test
        # Get board data for the current map
        board = get_board_data(mapNum)
        board_size = board.size

        # Create validator and solver objects
        validator = Validator()
        solver = Solver(validator)
        deducer = Deducer()

        algo_1_name = "Internal Deduction -> Brute Force Optimal Seed"
        # algo1 = internal_deduce_BFOS
        algo1 = internal_deduce_BF

        algo1_stats = run_algo(algo1, algo_1_name,mapNum,board,solver,validator,deducer)

        
        algo_2_name = "Internal + Row/Col Deduction Brute Force Optimal Seed"
        # algo2 = internal_rowcol_deduce_BFOS
        algo2 = internal_deduce_BFOS

        algo2_stats = run_algo(algo2, algo_2_name,mapNum,board,solver,validator,deducer)

        



        map_times[mapNum] = (algo1_stats, algo2_stats)

        image_path, boards_match = display_boards(map_times[mapNum],mapNum,image_folder)

        results.append([
            mapNum, f"{board_size}x{board_size}",
            f"{algo1_stats.elapsed:.6f}", algo1_stats.passed, algo1_stats.seeds_attempted, algo1_stats.chosen_seed,
            f"{algo2_stats.elapsed:.6f}", algo2_stats.passed, algo2_stats.seeds_attempted, algo2_stats.chosen_seed,
            "YES" if boards_match else "NO",
            image_path
        ])


        
        try:
            write_to_csv(csv_filename, results,algo_1_name,algo_2_name)
        except PermissionError:
            print(f"Warning: Could not save {csv_filename}. The file might be open. Skipping save...")

        print(f"Time Elapsed so far : {format_time(time.time() - begin_time)}")


    safe_write_to_csv(csv_filename, results, algo_1_name, algo_2_name)






    total_time = time.time() - begin_time
    print("\n-----------------------------------------------------------")
    print(f"Total Execution Time: {format_time(total_time)}")
    print("-----------------------------------------------------------")


# Run the main function
if __name__ == "__main__":
    main()
