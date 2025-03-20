from board import Board

class Validator:
    def __init__(self):
        pass

    def validate_win(self, board : Board):
        if self.validate_board(board):
            if len(board.queens) == board.size:
                print("YAY")
                return True
            
        return False

    def validate_board(self, board : Board):

        # Row/Col Constraints 
        rows_with_queens = set()
        cols_with_queens = set()


        for (row, col) in board.queens:
            if row in rows_with_queens or col in cols_with_queens:
                print("Row/Col Conflict")
                return False
            rows_with_queens.add(row)
            cols_with_queens.add(col)

        # Region Constraints
        regions_with_queens = set()

        for (row, col) in board.queens:
            region_id = board.region_map[row][col]
            if region_id in regions_with_queens:
                print(f"Region Conflict: {region_id}")
                return False
            regions_with_queens.add(region_id)


        # Immediate Diagonal

        for (row, col) in board.queens:
            for r_offset, c_offset in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
                neighbor_row = row + r_offset
                neighbor_col = col + c_offset



                if (0 <= neighbor_row < board.size) and (0 <= neighbor_col < board.size):
                    if (neighbor_row, neighbor_col) in board.queens:
                        print(f"Diagonal Neighbor Conflict")
                        return False
                
        return True
