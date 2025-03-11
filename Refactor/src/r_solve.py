from r_board import Board
from r_validation import Validator

class Solver:
    def __init__(self):
        self.validator = Validator()

    def brute_force_helper(self, board: Board, gui):
        """ Recursively solves the board using brute force. """

        # Base case: If the board is solved, return True
        if self.validator.validate_win(board):
            return True

        for row in range(board.size):
            for col in range(board.size):
                if (row, col) in board.queens or (row, col) in board.markers:
                    continue  # Skip already occupied positions
                
                # Place a queen and track the markers added
                new_markers = board.algo_autofill_queen(row, col)

                #gui.draw(board, False)  # Update GUI

                if self.brute_force_helper(board, gui):
                    return True  # Solution found!

                # Backtracking: Remove the queen and restore previous state
                board.remove_queen(row, col)
                for n_row, n_col in new_markers:
                    board.remove_marker(n_row, n_col)

                # board.place_marker(row, col)



                
                #gui.draw(board, False)  # Redraw board after backtracking

        return False  # No solution found at this level

    def brute_force(self, board: Board, gui):
        """ Initiates brute force solving. """

        for row in range(board.size):
            for col in range(board.size):
                if (row, col) in board.queens or (row, col) in board.markers:
                    continue  # Skip already occupied positions
                
                # Place a queen and track the markers added
                new_markers = board.algo_autofill_queen(row, col)

                gui.draw(board, False)  # Update GUI

                if self.brute_force_helper(board, gui):
                    return True  # Solution found!

                # Backtracking: Remove the queen and restore previous state
                board.remove_queen(row, col)
                for n_row, n_col in new_markers:
                    board.remove_marker(n_row, n_col)

                # board.place_marker(row,col)

        return False  # No solution found