import pygame
import random
import json
import os
import time

from board import Board
from validate import validate_board
from colors import WHITE,BLACK,RED,GREEN,REGION_COLORS

import solve



GRID_SIZE = 8
CELL_SIZE = 60
WINDOW_SIZE = GRID_SIZE * CELL_SIZE

MAPNUM = 100


pygame.init()

screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))

def get_window_size():
    return GRID_SIZE * CELL_SIZE




def get_board_data(mapNum: int):
    key = f"map{mapNum}"

    script_dir = os.path.dirname(os.path.abspath(__file__))  
    maps_file = os.path.join(script_dir, 'maps.json')

    
    with open(maps_file, "r") as file:
        data = json.load(file)
        
    mapData = data[key]
    
    return Board(mapData['name'], mapData['caseNumber'], mapData['colorGrid'])

def load_board(board_data: Board):
    global GRID_SIZE, CELL_SIZE, WINDOW_SIZE , screen
    
    GRID_SIZE = board_data.size
    CELL_SIZE = 600 // GRID_SIZE
    WINDOW_SIZE = GRID_SIZE * CELL_SIZE
    
    
    screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
    
              
            
        

def main():
    global GRID_SIZE, screen, regions, placed_queens, board
    
    board_data = get_board_data(MAPNUM)
    
    load_board(board_data)
    pygame.display.set_caption(f"Queen's Game - {board_data.name}")


    print(f"{board_data.name}")
    
    
    win = False

    attempt_solution = False

    running = True

    history = []

    while running:
        board_data.draw_board(screen, win)
        
        for event in pygame.event.get():
            
            
            
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x,y = event.pos

                col = x // CELL_SIZE
                row = y // CELL_SIZE

                if event.button == 1:  # Left click
                    board_data.player_modify_piece(row, col,-1)
                    win = validate_board(board_data)

                elif event.button == 3:  # Right click
                    board_data.player_modify_piece(row, col,1)
                    win = validate_board(board_data)

                elif event.button == 2:
                    board_data.queen_autofill(row, col,history)
                    win = validate_board(board_data)
                elif event.button == 4:
                    board_data.undo_last_autofill(history)
            
                    
            elif event.type == pygame.KEYDOWN:

                if event.key == pygame.K_q:
                    running = False

                if event.key == pygame.K_s:

                    start_time = time.time()

                    board_data = solve.brute_force(board_data,screen)

                    end_time = time.time()
                    elapsed = end_time - start_time
                    print(f"Solving took {elapsed:.4f} seconds")


                    win = validate_board(board_data)
                    

                
                


                
    
    
    pygame.quit()
    

    
    
    # # Initialize Pygame
    # pygame.init()
    # screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
    # pygame.display.set_caption("Queen's Game")


if __name__ == "__main__":
    main()


