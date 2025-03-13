from r_board import Board
from r_validation import Validator
import copy
from collections import defaultdict

class Solver:
    def __init__(self):
        self.validator = Validator()
        self.num_seeds = 0
        self.chosen_seed = (-1, -1)

    def brute_force_helper(self, board: Board, gui=None):
        """ Recursively solves the board using brute force. """

        # gui.draw(board,False)

        # Base case: If the board is solved, return True
        if self.validator.validate_win(board):
            return True

        for row in range(board.size):
            for col in range(board.size):
                
                if board.cell_is_empty(row, col):
                    
                    temp_queen, temp_marker = board.copy_pieces()
                    
                    board.algo_autofill_queen(row, col)
                    # board.player_autofill_queen(row, col)
                    # gui.draw(board, False)
                    
                    if self.brute_force_helper(board, gui):
                        return True
                    
                    else:
                        board.queens, board.markers = temp_queen, temp_marker
                        board.place_marker(row, col)
                        
                        return self.brute_force_helper(board,gui)

    def brute_force(self, board: Board, gui=None):
        """ Initiates brute force solving. """
        



        self.num_seeds = 0
        print("BRUTE FORCE")
        
        original = copy.deepcopy(board)

        
        for row in range(board.size):
            for col in range(board.size):
                
                if board.cell_is_empty(row, col):
                    
                    print(f"ATTEMPTING SEED: [{row}][{col}]")
                    self.num_seeds += 1
                    
                    attempt_board = copy.deepcopy(board)
                    attempt_board.algo_autofill_queen(row,col)
                    # attempt_board.player_autofill_queen(row,col)
                    
                    if self.brute_force_helper(attempt_board, gui):
                        board.copy(attempt_board)
                        
                        self.chosen_seed = (row, col)
                        
                        return True
                    
        return False
    
    
    def brute_force_optimal_seed(self, board: Board, gui=None):
        """ Initiates brute force solving. """
        



        self.num_seeds = 0
        print("BRUTE FORCE OPTIMAL SEED")
        
        original = copy.deepcopy(board)
        
                
        empty_cells = defaultdict(set)
        
        smalleset_region_id = -1
        least_cell_count = 15*15
        
        for region_id, cells in board.region_dict.items():
            if len(cells) < least_cell_count:
                least_cell_count = len(cells)
                smalleset_region_id = region_id
            
        empty_cells = board.region_dict[smalleset_region_id] - board.queens - board.markers
        print(smalleset_region_id)

        for (row, col) in empty_cells:
            
            
            if board.cell_is_empty(row, col):
                
                print(f"ATTEMPTING SEED: [{row}][{col}]")
                self.num_seeds += 1
                
                attempt_board = copy.deepcopy(board)
                attempt_board.algo_autofill_queen(row,col)
                # attempt_board.player_autofill_queen(row,col)
                
                if self.brute_force_helper(attempt_board, gui):
                    board.copy(attempt_board)
                    
                    self.chosen_seed = (row, col)
                    
                    return True
                    
        return False