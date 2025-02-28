import json
import pygame
from colors import WHITE,BLACK,RED,GREEN,REGION_COLORS


class Board:
    def __init__(self, name, size, regions):
        self.name = name
        self.size = size
        self.regions = regions

#         self.pieces = [
#     [1, -1, 1, -1, 1],
#     [-1, 1, -1, 1, -1],
#     [1, -1, 1, -1, 1],
#     [-1, 1, -1, 1, -1],
#     [1, -1, 1, -1, 1]
# ]
        
        self.pieces = [[0 for _ in range(size)] for _ in range(size)]
        


    def player_modify_piece(self, row, col, val):
        if 0 <= row < self.size and 0 <= col < self.size:

            # Toggle piece
            if self.pieces[row][col] == val:
                self.pieces[row][col] = 0

            else:
                self.pieces[row][col] = val
        else:
            print("Invalid position")
            
            
    def draw_board(self, screen, win = False):


        CELL_SIZE = 600 // self.size
        WINDOW_SIZE = CELL_SIZE * self.size

        padding = CELL_SIZE//10
        thickness = CELL_SIZE//40

        # Draw regions


        for row in range(self.size):
            for col in range(self.size):
                color_code = self.regions[row][col]
                color = REGION_COLORS[color_code]
                


                pygame.draw.rect(screen, color, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))


        # Draw pieces 
        for row in range(self.size):
            for col in range(self.size):
                if self.pieces[row][col] == 1:
                    pygame.draw.circle(screen, BLACK, (CELL_SIZE * col + CELL_SIZE // 2 , CELL_SIZE * row + CELL_SIZE // 2),CELL_SIZE//2-padding,thickness)
                elif self.pieces[row][col] == -1:
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
        for i in range(self.size + 1):
            pygame.draw.line(screen, grid_color, (i * CELL_SIZE, 0), (i * CELL_SIZE, WINDOW_SIZE), 2)  # Vertical
            pygame.draw.line(screen, grid_color, (0, i * CELL_SIZE), (WINDOW_SIZE, i * CELL_SIZE), 2)  # Horizontal
            
        pygame.display.flip()


    # No toggle, Force piece
    def algo_modify_piece(self, row, col, val):
        if 0 <= row < self.size and 0 <= col < self.size:

            self.pieces[row][col] = val
        # else:
        #     # print(f"Invalid position: [{row}][{col}]")

    def queen_autofill(self, queen_row, queen_col):

        region_id = self.regions[queen_row][queen_col]

              
        for row in range(self.size):
            for col in range(self.size):
                if row == queen_row and col == queen_col:
                    self.algo_modify_piece(row, col, 1)

                else:
                    if row == queen_row:
                        self.algo_modify_piece(row, col, -1)
                    elif col == queen_col:
                        self.algo_modify_piece(row, col, -1)
                    elif self.regions[row][col] == region_id:
                        self.algo_modify_piece(row,col,-1)

        self.algo_modify_piece(queen_row-1,queen_col-1,-1)
        self.algo_modify_piece(queen_row-1,queen_col+1,-1)
        self.algo_modify_piece(queen_row+1,queen_col-1,-1)
        self.algo_modify_piece(queen_row+1,queen_col+1,-1)

        


