import pygame
import time
# from board import Board
# from validate import Validator
# from solve import Solver
# from deduce import Deducer

import sys
sys.path.append('../data')
sys.path.append('.')

from colors import colors
from board import Board
from validation import Validator
from solve import Solver
from deduce import Deducer

class GUI:
    def __init__(self, caption, grid_size, cell_size, color_palette_name):
        self.GRID_SIZE = grid_size
        self.CELL_SIZE = cell_size
        self.WINDOW_SIZE = self.GRID_SIZE * self.CELL_SIZE

        self.color_palette = colors["REGION_COLORS"][color_palette_name]

        self.screen = pygame.display.set_mode((self.WINDOW_SIZE, self.WINDOW_SIZE))

        self.drag = False
        self.drag_place = False

        pygame.display.set_caption(caption)
        

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
                # If dragged, erase markers 
                self.drag_place = False
                board_data.remove_marker(row, col)
            else:
                # If dragged, place markers 
                self.drag_place = True
                board_data.place_marker(row, col)

        else:
            if (row, col) in board_data.markers:
                board_data.remove_marker(row, col)
                board_data.place_queen(row, col)
            elif (row, col) in board_data.queens:
                board_data.remove_queen(row, col)
            else:
                board_data.place_queen(row, col)
        
    def drag_markers(self, board_data : Board, row, col):

        # Do not edit queens pos when dragging
        if (row, col) in board_data.queens:
            return
        
        # Drag to place or remove markers
        if self.drag_place:
            board_data.place_marker(row, col)
        else:
            board_data.remove_marker(row, col)


        
    def handle_events(self, board_data: Board, validator: Validator, solver: Solver, deducer: Deducer, win: bool):
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False, win
            

            if event.type == pygame.MOUSEMOTION:
                if self.drag == True:
                    x, y = event.pos
                    col = x // self.CELL_SIZE
                    row = y // self.CELL_SIZE    

                    self.drag_markers(board_data, row, col)

            if event.type == pygame.MOUSEBUTTONUP:
                self.drag = False
                self.drag_place = False

            if event.type == pygame.MOUSEBUTTONDOWN:

                self.history.append(board_data.copy_pieces())

                x, y = event.pos
                col = x // self.CELL_SIZE
                row = y // self.CELL_SIZE

                if event.button == 1:  # Left click
                    if board_data.cell_is_queen(row, col):
                        self.drag = False
                    else:
                        self.drag = True
                    
                    self.toggle_pieces(board_data, 'X',row,col)

                elif event.button == 3:  # Right click
                    self.toggle_pieces(board_data, 'O',row,col)

                elif event.button == 2:  # Middle click
                    board_data.player_autofill_queen(row, col)


                # print(f"Queens: {board_data.queens}")
                # print(f"Markers: {board_data.markers}")

                win = validator.validate_win(board_data)



            # U - Undo
            # B - BRUTE FORCE
            # O - BFOS
            # D - Deduce
            # F - Full Deduce
            # S - Solve: Full Deduce -> BFOS
            if event.type == pygame.KEYDOWN:

                if event.key != pygame.K_u:
                    self.history.append(board_data.copy_pieces())
                    if event.key != pygame.K_r:
                        if not validator.validate_board(board_data):
                            print("Invalid Board State!!! Cannot deduce/solve")
                            continue


                if event.key == pygame.K_u:
                    if self.history:
                        print("UNDO!")
                        history = self.history.pop()
                        board_data.queens = history[0]
                        board_data.markers = history[1]
                        win = validator.validate_win(board_data)

                    else:
                        print("Nothing to undo")

                elif event.key == pygame.K_b:
                    win = solver.brute_force(board_data)
                    if not win:
                        print("NO SOLUTION FOUND FROM CURRENT BOARD STATE")
                        
                elif event.key == pygame.K_o:
                    win = solver.brute_force_optimal_seed(board_data)
                    if not win:
                        print("NO SOLUTION FOUND FROM CURRENT BOARD STATE")

                elif event.key == pygame.K_d:

                    start = time.time()
                    deducer.step_reduce_board(board_data)
                    elapsed = time.time() - start

                    win = validator.validate_win(board_data)

                    print(f"STEP DEDUCTION took {elapsed:.6f} seconds")

                elif event.key == pygame.K_f:

                    start = time.time()
                    deducer.full_reduce_board(board_data)
                    elapsed = time.time() - start

                    win = validator.validate_win(board_data)

                    print(f"FULL DEDUCTION took {elapsed:.6f} seconds")
                    win = validator.validate_win(board_data)
                
                elif event.key == pygame.K_s:
                    start = time.time()
                    deducer.full_reduce_board(board_data)
                    
                    win = solver.brute_force_optimal_seed(board_data)
                    elapsed = time.time() - start


                    print(f"DEDUCTION + BFOS took {elapsed:.6f} seconds")
                    
                elif event.key == pygame.K_q:
                    return False, win
                elif event.key == pygame.K_r:
                    board_data.reset_board()
                    print("RESET")
                    win = False


        return True, win
