import pygame
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

MAPNUM = 177#80 # 96 94


pygame.init()

screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))

def get_window_size():
    return GRID_SIZE * CELL_SIZE




def get_board_data(mapNum: int):
    key = f"map{mapNum}"

    maps_file = r"maps_data\maps.json"

    
    with open(maps_file, "r") as file:
        data = json.load(file)
        
    mapData = data[key]
    
    return Board(mapData['name'], mapData['caseNumber'], mapData['colorGrid'])


def get_board_data_archive(maps_file, mapNum: int):
    
    with open(maps_file, "r") as file:
        data = json.load(file)
        
    formatted_dict = {entry['id']: entry for entry in data}

    mapData = formatted_dict[mapNum]
    
    name = f"Map No {mapData['id']} - {mapData['date']}"
    size = len(mapData['grid'][0])
    region_map = mapData['regions']
    
    return Board(name, size, region_map)

def load_board(board_data: Board):
    global GRID_SIZE, CELL_SIZE, WINDOW_SIZE , screen
    
    GRID_SIZE = board_data.size
    CELL_SIZE = 600 // GRID_SIZE
    WINDOW_SIZE = GRID_SIZE * CELL_SIZE
    
    
    screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
    
              
MAP_PATH = R"maps_data\archivedqueens.json"
        

def main():
    global GRID_SIZE, screen, regions, placed_queens, board, MAPNUM
    
    # board_data = get_board_data(MAPNUM)
    board_data = get_board_data_archive(MAP_PATH, 315)
    
    
    validator = Validator()
    solver = Solver(validator)
    deducer = Deducer()
    
    load_board(board_data)
    pygame.display.set_caption(f"Queen's Game - {board_data.name}")


    print(f"{board_data.name}")
    
    
    win = False

    running = True
    while running:
        board_data.draw_board(screen, win)
        
        for event in pygame.event.get():
            board_data.draw_board(screen, win)
            
            
            
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

            

            # R - RESET
            # Q - QUIT
            # D - INTERNAL OVERLAP
            # E - n REGIONS       
            # A - FULL REDUCE
            # F - FULL REDUCE -> BFOS
            # C - Rol/col overlap             
            elif event.type == pygame.KEYDOWN:

                if event.key == pygame.K_q:
                    running = False
                   
                if event.key == pygame.K_r:
                    board_data.reset_board()
                    print("RESET")
                    win = False

                if event.key == pygame.K_d:                        
                    
                    start_time = time.time()

                    
                    overlap_X = deducer.internal_overlap(board_data)

                    end_time = time.time()
                    elapsed = end_time - start_time

                    print(f"Deduction took {elapsed:.4f} seconds")

                # if event.key == pygame.K_e:
                #     deducer.double_overlap(board_data)


                if event.key == pygame.K_c:
                    deducer.row_col_overlap(board_data)
                if event.key == pygame.K_e:
                    deducer.region_line_deduction(board_data)

                if event.key == pygame.K_a:                        
                    
                    start_time = time.time()

                    deducer.reduce_board_state(board_data)
                    
                    end_time = time.time()
                    elapsed = end_time - start_time

                    print(f"FULL Deduction took {elapsed:.4f} seconds")

                    win = validator.validate_win(board_data)
                    if win:
                        board_data.draw_board(screen, win)

                if event.key == pygame.K_f:
                    start_time = time.time()
                    
                    deducer.reduce_board_state(board_data)
                    board_data = solver.brute_force_optimal_seed(board_data)
                    win = validator.validate_win(board_data)


                    end_time = time.time()
                    elapsed = end_time - start_time
                    print(f"FULL SOLUTION took {elapsed:.4f} seconds")
                    

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
                        
                        # board_data.solve_autofill()
                        # board_data.draw_board(screen)
                        

                        start_time = time.time()

                        board_data = algo(board_data)

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


