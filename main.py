import pygame
import random
import json
import os
import time

from board import Board
from validate import Validator
from colors import WHITE,BLACK,RED,GREEN,REGION_COLORS

from solve import Solver
from deduce import Deducer



GRID_SIZE = 8
CELL_SIZE = 60
WINDOW_SIZE = GRID_SIZE * CELL_SIZE

MAPNUM = 80 # 94


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
    global GRID_SIZE, screen, regions, placed_queens, board, MAPNUM
    
    board_data = get_board_data(MAPNUM)
    validator = Validator()
    solver = Solver(validator)
    deducer = Deducer()
    
    load_board(board_data)
    pygame.display.set_caption(f"Queen's Game - {board_data.name}")


    print(f"{board_data.name}")
    
    
    win = False

    attempt_solution = False

    running = True
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
                    win = validator.validate_win(board_data)

                elif event.button == 3:  # Right click
                    board_data.player_modify_piece(row, col,1)
                    win = validator.validate_win(board_data)
                    
                elif event.button == 2:
                    board_data.queen_autofill(row, col)
                    win = validator.validate_win(board_data)

            
                    
            elif event.type == pygame.KEYDOWN:

                if event.key == pygame.K_q:
                    running = False

                if event.key == pygame.K_n:
                    MAPNUM += 1
                    board_data = get_board_data(MAPNUM)
                    pygame.display.set_caption(f"Queen's Game - {board_data.name}")

                    
                if event.key == pygame.K_r:
                    board_data.reset_board()
                    win = False

                if event.key == pygame.K_d:                        
                    
                    start_time = time.time()

                    # deduction = True

                    # while(deduction):
                    #     deduction = deducer.all_overlap(board_data)
                    
                    
                    
                    overlap_X = deducer.internal_overlap(board_data)

                    end_time = time.time()
                    elapsed = end_time - start_time

                    print(f"Deduction took {elapsed:.4f} seconds")

                # if event.key == pygame.K_e:
                #     deducer.double_overlap(board_data)



                if event.key == pygame.K_o or event.key == pygame.K_s:

                    if win:
                        print("BOARD ALREADY SOLVED, RESET WITH R")
                        continue

                    print(f"\nATTEMPTING SOLUTION WITH ALGO: ")
                    if event.key == pygame.K_s:
                        algo = solver.brute_force
                    else:
                        algo = solver.brute_force_optimal_seed
                    
                   
                    if validator.validate_board(board_data):
                        
                        board_data.solve_autofill()
                        board_data.draw_board(screen)
                        

                        start_time = time.time()

                        board_data = algo(board_data,screen)

                        end_time = time.time()
                        elapsed = end_time - start_time
                        
                        win = validator.validate_win(board_data)
                        
                        if win:
                            print(f"Solving took {elapsed:.4f} seconds")
                        else:
                            print(f"Attempt took {elapsed:.4f} seconds")
                            


                        
                        
                    else:
                        print("Invalid Board State")
                    

                
                


                
    
    
    pygame.quit()
    

    
    
    # # Initialize Pygame
    # pygame.init()
    # screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
    # pygame.display.set_caption("Queen's Game")


if __name__ == "__main__":
    main()


