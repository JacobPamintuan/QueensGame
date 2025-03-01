from board import Board
from validate import Validator
from solve import Solver
import copy
import os
import json
import time
import csv
import os

import pygame
#  map_times[mapNum] = (
#             elapsed_BF, 
#             solved_BF,  # Boolean indicating if Algorithm 1 solved the map
#             num_seeds_BF,
#             attempt_BF,
#             elapsed_BFOS, 
#             solved_BFOS,  # Boolean indicating if Algorithm 2 solved the map
#             num_seeds_BFOS,
#             attempt_BFOS # The actual board object
#         )
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



def display_boards(map_stats, image_folder):
    pygame.init()
    pygame.font.init()

    algo1_stats, algo2_stats = map_stats  # Unpack the tuple

    grid_size = algo1_stats.board.size
    CELL_SIZE = 600 // grid_size  # Keep cell size within reasonable bounds

    WINDOW_SIZE = grid_size * CELL_SIZE
    WINDOW_PADDING = 30  
    screen_width = (WINDOW_SIZE * 2) + WINDOW_PADDING + 10  
    screen_height = WINDOW_SIZE + 150  # Extra height for text display

    screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
    pygame.display.set_caption(f"Comparison - Map {algo1_stats.board.name}")

    # running = True
    # while running:
    screen.fill((255, 255, 255))
    font = pygame.font.Font(None, 24)

    # Draw captions above each board
    caption_algo1 = font.render(f"{algo1_stats.algo_name} - Algo 1", True, (0, 0, 0))
    caption_algo2 = font.render(f"{algo2_stats.algo_name} - Algo 2", True, (0, 0, 0))

    screen.blit(caption_algo1, (WINDOW_SIZE // 2 - caption_algo1.get_width() // 2, 10))
    screen.blit(caption_algo2, (WINDOW_SIZE + WINDOW_PADDING + (WINDOW_SIZE // 2 - caption_algo2.get_width() // 2), 10))

    # Draw boards
    algo1_stats.board.draw_board(screen.subsurface((0, 50, WINDOW_SIZE, WINDOW_SIZE)), algo1_stats.passed)
    algo2_stats.board.draw_board(screen.subsurface((WINDOW_SIZE + WINDOW_PADDING, 50, WINDOW_SIZE, WINDOW_SIZE)), algo2_stats.passed)

    # Display additional information
    info_start_y = WINDOW_SIZE + 60
    info_x = 20

    stats = [
        f"Algo 1 | Time: {algo1_stats.elapsed:.4f}s | Solved: {algo1_stats.passed} | Seeds: {algo1_stats.seeds_attempted} | Seed: {algo1_stats.chosen_seed}",
        f"Algo 2 | Time: {algo2_stats.elapsed:.4f}s | Solved: {algo2_stats.passed} | Seeds: {algo2_stats.seeds_attempted} | Seed: {algo2_stats.chosen_seed}",
    ]

    for i, stat in enumerate(stats):
        stat_text = font.render(stat, True, (0, 0, 0))
        screen.blit(stat_text, (info_x, info_start_y + (i * 25)))

    pygame.display.flip()

    # Save the image
    image_path = os.path.join(image_folder, f"comparison_map_{algo1_stats.board.name}.png")
    pygame.image.save(screen, image_path)

        # Event handling
        # for event in pygame.event.get():
        #     if event.type == pygame.QUIT:
        # running = False

        # time.sleep(2)  # Show the boards for 2 seconds
        # running = False

    pygame.quit()

    return image_path


def run_algo(algo_fn, algo_name, mapNum, board : Board, solver : Solver, validator : Validator):
    print("\n-----------------------------------------------------------")
    print(f"MAP #{mapNum}")

    # Timing and executing the brute force algorithm
    print(f"Running {algo_name} algorithm...")

    start_time = time.time()
    final_board = algo_fn(board, None)
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




def write_to_csv(filename, results):
    """Overwrites the CSV file with all results at once."""
    with open(filename, mode="w", newline="") as file:  # "w" mode to overwrite
        writer = csv.writer(file)

        # Write header
        writer.writerow([
            "Map", 
            "BF Time (s)", "BF Solved", "BF Seeds", "BF Chosen Seed",
            "BFOS Time (s)", "BFOS Solved", "BFOS Seeds", "BFOS Chosen Seed",
            "Image Path"
        ])

        # Write all results from the list
        writer.writerows(results)


def safe_write_to_csv(filename, results):
    """Tries to write to the CSV file, prompting the user if the file is open."""
    while True:
        try:
            write_to_csv(filename, results)
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

# Initialize the dictionary to store map data
map_times = {}

def main():

    image_folder = "test"

    os.makedirs(image_folder, exist_ok=True)
    csv_filename = os.path.join(image_folder, "output.csv")


    results = []

    begin_time = time.time()

     # Define the specific maps to test (instead of iterating over all 100)
    for mapNum in [1, 6, 67, 80, 89]:  # Maps you want to test
        # Get board data for the current map
        board = get_board_data(mapNum)

        # Create validator and solver objects
        validator = Validator()
        solver = Solver(validator)

        algo_1_name = "Brute Force"
        algo1 = solver.brute_force

        algo1_stats = run_algo(algo1, algo_1_name,mapNum,board,solver,validator)

        
        algo_2_name = "Brute Force Optimal Seed"
        algo2 = solver.brute_force_optimal_seed

        algo2_stats = run_algo(algo2, algo_2_name,mapNum,board,solver,validator)

        



        map_times[mapNum] = (algo1_stats, algo2_stats)

        image_path = display_boards(map_times[mapNum],image_folder)

        results.append([
            mapNum,
            f"{algo1_stats.elapsed:.6f}", algo1_stats.passed, algo1_stats.seeds_attempted, algo1_stats.chosen_seed,
            f"{algo2_stats.elapsed:.6f}", algo2_stats.passed, algo2_stats.seeds_attempted, algo2_stats.chosen_seed,
            image_path  # Store the image path in the CSV
        ])


        
        try:
            write_to_csv(csv_filename, results)
        except PermissionError:
            print(f"Warning: Could not save {csv_filename}. The file might be open. Skipping save...")

        print(f"Time Elapsed so far : {format_time(time.time() - begin_time)}")


    safe_write_to_csv(csv_filename, results)


    # After processing all maps, print the results
    print("\n-----------------------------------------------------------")
    print("Results after processing all maps:")

    for mapNum, (algo1_stats, algo2_stats) in map_times.items():
        print(f"\nMap {mapNum}:")
        print(f"  {algo1_stats.algo_name}:")
        print(f"    - Time Taken: {algo1_stats.elapsed:.6f}s")
        print(f"    - Solved: {algo1_stats.passed}")
        print(f"    - Seeds Attempted: {algo1_stats.seeds_attempted}")
        print(f"    - Chosen Seed: {algo1_stats.chosen_seed}")
        # print(f"    - Final Board State: {algo1_stats.board.pieces}")

        print(f"\n  {algo2_stats.algo_name}:")
        print(f"    - Time Taken: {algo2_stats.elapsed:.6f}s")
        print(f"    - Solved: {algo2_stats.passed}")
        print(f"    - Seeds Attempted: {algo2_stats.seeds_attempted}")
        print(f"    - Chosen Seed: {algo2_stats.chosen_seed}")
        # print(f"    - Final Board State: {algo2_stats.board.pieces}")

    print("\n-----------------------------------------------------------")


    total_time = time.time() - begin_time
    print("\n-----------------------------------------------------------")
    print(f"Total Execution Time: {format_time(total_time)}")
    print("-----------------------------------------------------------")


# Run the main function
if __name__ == "__main__":
    main()
