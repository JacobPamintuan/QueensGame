import pygame
import time
# from board import Board
# from validate import Validator
# from solve import Solver
# from deduce import Deducer

import sys
sys.path.append('../data')
sys.path.append('.')

from Refactor.data.colors import colors
from r_board import Board
from r_validation import Validator
from r_solve import Solver

class GUI:
    def __init__(self, grid_size, cell_size, color_palette_name):
        self.GRID_SIZE = grid_size
        self.CELL_SIZE = cell_size
        self.WINDOW_SIZE = self.GRID_SIZE * self.CELL_SIZE

        self.color_palette = colors["REGION_COLORS"][color_palette_name]

        self.screen = pygame.display.set_mode((self.WINDOW_SIZE, self.WINDOW_SIZE))
        pygame.display.set_caption("Queen's Game")
        

        self.history = []

    def update_window_size(self, grid_size):
        self.GRID_SIZE = grid_size
        self.CELL_SIZE = 600 // self.GRID_SIZE
        self.WINDOW_SIZE = self.GRID_SIZE * self.CELL_SIZE
        self.screen = pygame.display.set_mode((self.WINDOW_SIZE, self.WINDOW_SIZE))

    def draw(self, board_data : Board, win):
        padding = self.CELL_SIZE//10
        thickness = self.CELL_SIZE//40

        
        # Draw regions


        for row in range(board_data.size):
            for col in range(board_data.size):
                color_code = board_data.region_map[row][col]
                color = self.color_palette[color_code]
                


                pygame.draw.rect(self.screen, color, (col * self.CELL_SIZE, row * self.CELL_SIZE, self.CELL_SIZE, self.CELL_SIZE))


        for row,col in board_data.queens:
            pygame.draw.circle(self.screen, colors["BLACK"], (self.CELL_SIZE * col + self.CELL_SIZE // 2 , self.CELL_SIZE * row + self.CELL_SIZE // 2),self.CELL_SIZE//2-padding,thickness)

        for row,col in board_data.markers:
            pygame.draw.line(self.screen, colors["BLACK"],
                                (col * self.CELL_SIZE + padding, row * self.CELL_SIZE + padding), 
                                ((col+1)*self.CELL_SIZE - padding, (row+1)*self.CELL_SIZE - padding),
                                thickness) 
            
            pygame.draw.line(self.screen, colors["BLACK"],
                                (col * self.CELL_SIZE + padding, (row+1) * self.CELL_SIZE - padding), 
                                ((col+1)*self.CELL_SIZE - padding, row*self.CELL_SIZE + padding),
                                thickness) 


    
        if win:
            grid_color = colors["GREEN"]
        else:
            grid_color = colors["BLACK"] 
        # Draw gridlines
        for i in range(board_data.size + 1):
            pygame.draw.line(self.screen, grid_color, (i * self.CELL_SIZE, 0), (i * self.CELL_SIZE, self.WINDOW_SIZE), 2)  # Vertical
            pygame.draw.line(self.screen, grid_color, (0, i * self.CELL_SIZE), (self.WINDOW_SIZE, i * self.CELL_SIZE), 2)  # Horizontal
            
        pygame.display.flip()


    def toggle_pieces(self, board_data : Board, type, row, col):


        if type == 'X':
            if (row, col) in board_data.queens:
                board_data.remove_queen(row, col)
                board_data.place_marker(row, col)
            elif (row, col) in board_data.markers:
                board_data.remove_marker(row, col)
            else:
                board_data.place_marker(row, col)

        else:
            if (row, col) in board_data.markers:
                board_data.remove_marker(row, col)
                board_data.place_queen(row, col)
            elif (row, col) in board_data.queens:
                board_data.remove_queen(row, col)
            else:
                board_data.place_queen(row, col)


        
    def handle_events(self, board_data : Board, validator : Validator, solver: Solver, win):
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False, win
            elif event.type == pygame.MOUSEBUTTONDOWN:

                self.history.append(board_data.copy())

                x, y = event.pos
                col = x // self.CELL_SIZE
                row = y // self.CELL_SIZE

                if event.button == 1:  # Left click
                    self.toggle_pieces(board_data, 'X',row,col)
                    

                elif event.button == 3:  # Right click
                    self.toggle_pieces(board_data, 'O',row,col)

                elif event.button == 2:  # Middle click
                    board_data.player_autofill_queen(row, col)


                print(f"Queens: {board_data.queens}")
                print(f"Markers: {board_data.markers}")

                win = validator.validate_win(board_data)

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_u:
                    if self.history:
                        print("UNDO!")
                        history = self.history.pop()
                        board_data.queens = history[0]
                        board_data.markers = history[1]
                    else:
                        print("Nothing to undo")

                if event.key == pygame.K_b:
                    solver.brute_force(board_data, self)
                
                elif event.key == pygame.K_q:
                    return False, win
                elif event.key == pygame.K_r:
                    board_data.reset_board()
                    print("RESET")
                    win = False

        return True, win
