import pygame
import random
import json
import os

from board import Board
from validate import validate_board
from colors import WHITE,BLACK,RED,GREEN,REGION_COLORS


GRID_SIZE = 8
CELL_SIZE = 60
WINDOW_SIZE = GRID_SIZE * CELL_SIZE




pygame.init()

screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
pygame.display.set_caption("Queen's Game")

def get_window_size():
    return GRID_SIZE * CELL_SIZE



# class Board:
#     def __init__(self, name, size, regions):
#         self.name = name
#         self.size = size
#         self.regions = regions

#         self.pieces = [
#     [1, -1, 1, -1, 1],
#     [-1, 1, -1, 1, -1],
#     [1, -1, 1, -1, 1],
#     [-1, 1, -1, 1, -1],
#     [1, -1, 1, -1, 1]
# ]#[[-1 for _ in range(size)] for _ in range(size)]
        


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
    
    board_data = get_board_data(1)
    
    load_board(board_data)
    
    
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
                    board_data.modify_piece(row, col,-1)
                    win = validate_board(board_data)

                elif event.button == 3:  # Right click
                    board_data.modify_piece(row, col,1)
                    win = validate_board(board_data)
                    
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    attempt_solution = True
                    

                
                


                
    
    
    pygame.quit()
    

    
    
    # # Initialize Pygame
    # pygame.init()
    # screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
    # pygame.display.set_caption("Queen's Game")


if __name__ == "__main__":
    main()


