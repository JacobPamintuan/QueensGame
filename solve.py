from board import Board
from validate import validate_move, validate_board
import copy
import pdb

def brute_force_helper(board_data, screen, history):
    # board_data.draw_board(screen)

    if validate_board(board_data):
        return True  # Found a valid configuration

    for row in range(board_data.size):
        for col in range(board_data.size):
            if board_data.pieces[row][col] == 0:  # If cell is empty

                # Save current state and attempt to place a queen
                board_data.queen_autofill(row, col, history)

                # Recurse to the next step
                if brute_force_helper(board_data, screen, history):
                    return True  # Valid solution found

                # Undo the autofill and backtrack
                board_data.undo_last_autofill(history)
                # board_data.draw_board(screen, False)

    return False  # No valid configuration found


def brute_force(board_data, screen):
    history = []  # Initialize history stack

    for row in range(board_data.size):
        for col in range(board_data.size):

            print(f"Trying to place a queen at [{row}][{col}]")

            # Copy the board to avoid side-effects (if needed) – Optional for this case
            temp = copy.deepcopy(board_data)

            # Try autofill with the queen in the current position and track changes
            temp.queen_autofill(row, col, history)

            # Draw the board for visualization
            # temp.draw_board(screen, False)

            # Call the helper function to solve the board from this point
            attempt = brute_force_helper(temp, screen, history)

            # If a solution was found, apply the result to the main board
            if attempt:
                board_data = copy.deepcopy(temp)
                return board_data  # Return the solved board

            # Reset the temporary board for the next attempt
            # temp.draw_board(screen, False)

    print("No solution found!")
    return board_data  # No solution found, return the initial board (or handle as needed)
