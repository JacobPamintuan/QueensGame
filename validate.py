from board import Board
import numpy as np

def validate_board(board_data : Board):
    

    pieces_array = np.array(board_data.pieces)


    positive_col_sums = np.sum(pieces_array * (pieces_array > 0), axis=0)
    positive_row_sums = np.sum(pieces_array * (pieces_array > 0), axis=1)

    # More than one queen per row or col
     
    if np.any(positive_col_sums > 1) or np.any(positive_row_sums > 1): 

        # print("row/col")
        return False
    
    regions_with_queens = []

    for row in range(board_data.size):
        for col in range(board_data.size):
            if board_data.pieces[row][col] == 1:
                regions_with_queens.append(board_data.regions[row][col])


    if len(regions_with_queens) != len(set(regions_with_queens)):
        # print("dup")
        return False
    
    if len(set(regions_with_queens)) == board_data.size:
        print("YAY")
        return True
