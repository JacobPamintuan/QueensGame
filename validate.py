from board import Board
import numpy as np

class Validator:
    def __init__(self):
        pass

    def check_diagonals(self,board_data : Board, q_row, q_col):
            
            for i in [-1,1]:
                for j in [-1,1]:
                    row = q_row + i
                    col = q_col + j
                    if 0 <= row < board_data.size and 0 <= col < board_data.size:
                        if board_data.pieces[row][col] == 1:
                            return False
                        
            
            return True


        
    def validate_win(self,board_data : Board):
        

        pieces_array = np.array(board_data.pieces)


        positive_col_sums = np.sum(pieces_array * (pieces_array > 0), axis=0)
        positive_row_sums = np.sum(pieces_array * (pieces_array > 0), axis=1)

        # More than one queen per row or col
        
        if np.any(positive_col_sums > 1) or np.any(positive_row_sums > 1): 

            print("row/col")
            return False
        
        
        # One queen per region
        regions_with_queens = []

        for row in range(board_data.size):
            for col in range(board_data.size):
                if board_data.pieces[row][col] == 1:
                    regions_with_queens.append(board_data.region_map[row][col])
                    
                    if not self.check_diagonals(board_data, row, col):
                        print("Diagonal")
                        return False


        if len(regions_with_queens) != len(set(regions_with_queens)):
            print("dup")
            return False
        
        
        
        if len(set(regions_with_queens)) == board_data.size:
            print("YAY")
            return True
        
        
    def validate_board(self, board_data : Board):
        

        pieces_array = np.array(board_data.pieces)


        positive_col_sums = np.sum(pieces_array * (pieces_array > 0), axis=0)
        positive_row_sums = np.sum(pieces_array * (pieces_array > 0), axis=1)

        # More than one queen per row or col
        
        if np.any(positive_col_sums > 1) or np.any(positive_row_sums > 1): 

            print("row/col")
            return False
        
        
        # One queen per region
        regions_with_queens = []

        for row in range(board_data.size):
            for col in range(board_data.size):
                if board_data.pieces[row][col] == 1:
                    regions_with_queens.append(board_data.region_map[row][col])
                    
                    if not self.check_diagonals(board_data, row, col):
                        print("Diagonal")
                        return False


        if len(regions_with_queens) != len(set(regions_with_queens)):
            print("dup")
            return False
        
        
        return True


    def validate_move(board_data : Board, row, col):
        

        pieces_array = np.array(board_data.pieces)


        positive_col_sums = np.sum(pieces_array * (pieces_array > 0), axis=0)
        positive_row_sums = np.sum(pieces_array * (pieces_array > 0), axis=1)
        
        if positive_row_sums[row] >= 1 or positive_col_sums[col] >= 1:
            return False

        # More than one queen per row or col
        
        if np.any(positive_col_sums > 1) or np.any(positive_row_sums > 1): 

            # print("row/col")
            return False
        
        regions_with_queens = []

        for row in range(board_data.size):
            for col in range(board_data.size):
                if board_data.pieces[row][col] == 1:
                    regions_with_queens.append(board_data.region_map[row][col])


        if len(regions_with_queens) != len(set(regions_with_queens)):
            # print("dup")
            return False
        

        return True