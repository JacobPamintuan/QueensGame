from board import Board
from validate import Validator
from solve import Solver
import os
import json
import time


import pygame

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


def display_boards(BF_board: Board, BF_pass, BFOS_board: Board, BFOS_pass, image_folder):
    pygame.init()
    pygame.font.init()
    """Displays both the original and solved boards side by side using Pygame."""
    grid_size = BF_board.size

    CELL_SIZE = 600//grid_size  # Keep cell size within reasonable bounds

    WINDOW_SIZE = grid_size * CELL_SIZE
    WINDOW_PADDING = 30  # Increase padding slightly
    screen_width = (WINDOW_SIZE * 2) + WINDOW_PADDING + 10  # Ensure enough width
    screen_height = WINDOW_SIZE + 60  # Add extra space for captions

    screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
    pygame.display.set_caption("Auto Tester - Comparing Boards")

    running = True
    while running:
        screen.fill((255, 255, 255))
        font = pygame.font.Font(None, 36)
        
        # Draw captions above each board
        caption_BF = font.render("Brute Force", True, (0, 0, 0))
        caption_BFOS = font.render("Brute Force Optimal Seed", True, (0, 0, 0))
        
        screen.blit(caption_BF, (WINDOW_SIZE // 2 - caption_BF.get_width() // 2, 10))
        screen.blit(caption_BFOS, (WINDOW_SIZE + WINDOW_PADDING + (WINDOW_SIZE // 2 - caption_BFOS.get_width() // 2), 10))
        
        # Draw boards below captions
        BF_board.draw_board(screen.subsurface((0, 50, WINDOW_SIZE, WINDOW_SIZE)),BF_pass)
        BFOS_board.draw_board(screen.subsurface((WINDOW_SIZE + WINDOW_PADDING, 50, WINDOW_SIZE, WINDOW_SIZE)),BFOS_pass)
        
        pygame.display.flip()
        

        image_path = os.path.join(image_folder, f"comparison_map_{BF_board.name}.png")

        pygame.image.save(screen, image_path)  # Save the screen as a PNG file with map name

        # Event loop to allow closing the window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        time.sleep(2)  # Show the boards for 2 seconds before proceeding
        running = False  # Exit loop after delay

    pygame.quit()




# Initialize the dictionary to store map data
map_times = {}

def main():

    image_folder = "Images"

     # Define the specific maps to test (instead of iterating over all 100)
    for mapNum in [1]:#, 6, 67, 80, 89]:  # Maps you want to test
        # Get board data for the current map
        board = get_board_data(mapNum)

        # Create validator and solver objects
        validator = Validator()
        solver = Solver(validator)

        print("\n-----------------------------------------------------------")
        print(f"MAP #{mapNum}")

        # Timing and executing the brute force algorithm
        print("Running Brute Force algorithm...")
        start_BF = time.time()
        attempt_BF = solver.brute_force(board, None)
        end_BF = time.time()
        elapsed_BF = end_BF - start_BF  # Time taken for brute_force
        print(f"Brute Force Time: {elapsed_BF:.4f}s")

        solved_BF = validator.validate_win(attempt_BF)  # Validation result for brute_force
        print(f"Brute Force Solved: {solved_BF}")

        num_seeds_BF = solver.num_seeds
        print(f"Brute Force Seeds Attempted: {num_seeds_BF}")


        # Timing and executing the brute force optimal seed algorithm
        print("Running Brute Force with Optimal Seed algorithm...")
        start_BFOS = time.time()
        attempt_BFOS = solver.brute_force_optimal_seed(board, None)
        end_BFOS = time.time()
        elapsed_BFOS = end_BFOS - start_BFOS  # Time taken for brute_force_optimal_seed
        print(f"Brute Force with Optimal Seed Time: {elapsed_BFOS:.4f}s")

        solved_BFOS = validator.validate_win(attempt_BFOS)  # Validation result for brute_force_optimal_seed
        print(f"Brute Force with Optimal Seed Solved: {solved_BFOS}")

        num_seeds_BFOS = solver.num_seeds
        print(f"Brute Force Seeds Attempted: {num_seeds_BFOS}")

        display_boards(attempt_BF,solved_BF, attempt_BFOS,solved_BFOS, image_folder)

        # Storing map data: (time_BF, result_BF, time_BFOS, result_BFOS, board)
        print(f"Storing data for map #{mapNum}...")
        map_times[mapNum] = (
            elapsed_BF, 
            solved_BF,  # Boolean indicating if Algorithm 1 solved the map
            num_seeds_BF,
            attempt_BF.pieces,
            elapsed_BFOS, 
            solved_BFOS,  # Boolean indicating if Algorithm 2 solved the map
            num_seeds_BFOS,
            attempt_BFOS.pieces  # The actual board object
        )

    # After processing all maps, print or return the results
    print("\n-----------------------------------------------------------")
    print("Results after processing all maps:")
    for mapNum, (time_BF, result_BF, num_seeds_BF, pieces_BF, time_BFOS, result_BFOS, num_seeds_BFOS, pieces_BFOS) in map_times.items():
        print(f"Map {mapNum}:")
        print(f"  Brute Force: Time = {time_BF:.4f}s, Solved = {result_BF}, Seeds Attempted = {num_seeds_BF}")
        print(f"  Brute Force with Optimal Seed: Time = {time_BFOS:.4f}s, Solved = {result_BFOS}, Seeds Attempted = {num_seeds_BFOS}")
        print(f"  Board (Brute Force Pieces): {pieces_BF}")  # Print the pieces from brute force attempt
        print(f"  Board (Brute Force with Optimal Seed Pieces): {pieces_BFOS}")  # Print the pieces from optimal seed attempt

# Run the main function
if __name__ == "__main__":
    main()
