import pygame
import random
import json
import os

from board import Board
from validate import validate_board

GRID_SIZE = 8
CELL_SIZE = 60
WINDOW_SIZE = GRID_SIZE * CELL_SIZE

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)  
GREEN = (0, 255, 0)

REGION_COLORS = [
    (179, 223, 160),    # Light Green
    (163,210,216),      # Light Blue
    (255,123,96),       # Light Red
    (255,201,146),      # Light Orange
    (223,160,191),      # Pink
    (150,190,255),      # Light Blue
    (223,223,223),      # Grey
    (230,243,136)       # Yellow       
    ]


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
    
    
    
def draw_board(board_data : Board, win : bool):
    
    # Draw regions


    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            color_code = board_data.regions[row][col]
            color = REGION_COLORS[color_code]
            


            pygame.draw.rect(screen, color, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    padding = CELL_SIZE//10
    thickness = CELL_SIZE//40

    # Draw pieces 
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            if board_data.pieces[row][col] == 1:
                pygame.draw.circle(screen, BLACK, (CELL_SIZE * col + CELL_SIZE // 2 , CELL_SIZE * row + CELL_SIZE // 2),CELL_SIZE//2-padding,thickness)
            elif board_data.pieces[row][col] == -1:
                pygame.draw.line(screen, BLACK,
                                    (col * CELL_SIZE + padding, row * CELL_SIZE + padding), 
                                    ((col+1)*CELL_SIZE - padding, (row+1)*CELL_SIZE - padding),
                                    thickness) 
                
                pygame.draw.line(screen, BLACK,
                                    (col * CELL_SIZE + padding, (row+1) * CELL_SIZE - padding), 
                                    ((col+1)*CELL_SIZE - padding, row*CELL_SIZE + padding),
                                    thickness) 
                

   
    if win:
        grid_color = GREEN
    else:
        grid_color = BLACK 
    # Draw gridlines
    for i in range(GRID_SIZE + 1):
        pygame.draw.line(screen, grid_color, (i * CELL_SIZE, 0), (i * CELL_SIZE, WINDOW_SIZE), 2)  # Vertical
        pygame.draw.line(screen, grid_color, (0, i * CELL_SIZE), (WINDOW_SIZE, i * CELL_SIZE), 2)  # Horizontal
        
    pygame.display.flip()
        

            
            
        

def main():
    global GRID_SIZE, screen, regions, placed_queens, board
    
    board_data = get_board_data(1)
    
    load_board(board_data)
    
    
    win = False

    running = True
    while running:
        draw_board(board_data, win)
        
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





                
                


                
    
    
    pygame.quit()
    

    
    
    # # Initialize Pygame
    # pygame.init()
    # screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
    # pygame.display.set_caption("Queen's Game")


if __name__ == "__main__":
    main()


