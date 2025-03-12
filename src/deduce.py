from src.board import Board
import copy 

from collections import defaultdict
class Deducer:
    def __init__(self):
        pass

    def get_X_positions(self, board : Board):

        pos_list = []

        for row in range(board.size):
            for col in range(board.size):
                if board.pieces[row][col] == -1:
                    pos_list.append((row,col))

        return set(pos_list)

    def determine_internal_overlap(self, board : Board, region_id):
        test_board = copy.deepcopy(board)
        # test_board.reset_board()

        X_positions = []
        for cell in board.region_dict[region_id]:
            test_board.queen_autofill(cell[0],cell[1])


            # Add positions that became an X after placing a queen
            X_positions.append(self.get_X_positions(test_board))
            test_board = copy.deepcopy(board)

        common_coords = set.intersection(*X_positions)
        #print(f"{region_id}: {common_coords}")
        return common_coords


    def internal_overlap(self, board :Board):
        overlap = []

        prev_board = copy.deepcopy(board)

        for region_id in board.region_dict.keys():
            common_coords = self.determine_internal_overlap(board, region_id)

            if common_coords:
                overlap.append(common_coords)

        if overlap:

            overlap = set.union(*overlap)
        
        for row, col in overlap:
            board.place_piece(row,col,-1)

        # for coord_sets in overlap:
        #     for row, col in coord_sets:
        #         board.place_piece(row,col,-1)
                
        if board.pieces == prev_board.pieces:
            print("NO FURTHER INTERNAL DEDUCTIONS")
            return False
        
        return True

        # #print(overlap)
        # return overlap
        

    def determine_rowcol_overlap(self, board : Board, line):
        test_board = copy.deepcopy(board)
        # test_board.reset_board()

        row_X_positions = []
        row_Y_positions = []
        
        for col in range(board.size):
            if board.pieces[line][col] == 0:
                test_board.queen_autofill(line, col)


                # Add positions that became an X after placing a queen
                row_X_positions.append(self.get_X_positions(test_board))
                test_board = copy.deepcopy(board)

        common_row_coords = []
        if row_X_positions:
            common_row_coords = set.intersection(*row_X_positions)

        for row in range(board.size):
            if board.pieces[row][line] == 0:
                test_board.queen_autofill(row, line)


                # Add positions that became an X after placing a queen
                row_Y_positions.append(self.get_X_positions(test_board))
                test_board = copy.deepcopy(board)

        common_col_coords = []
        if row_Y_positions:
            common_col_coords = set.intersection(*row_Y_positions)


        return common_row_coords, common_col_coords

    def row_col_overlap(self, board : Board):
        overlap = []

        original_board = copy.deepcopy(board)

        for line in range(board.size):
            row_coords, col_coords = self.determine_rowcol_overlap(board, line)

            if row_coords: overlap.append(row_coords)
            if col_coords: overlap.append(col_coords)


        if overlap:

            overlap = set.union(*overlap)
        
        for row, col in overlap:
            board.place_piece(row,col,-1)

        # for coord_sets in overlap:
        #     for row, col in coord_sets:
        #         board.place_piece(row,col,-1)
                
        if board.pieces == original_board.pieces:
            print("NO FURTHER ROW/COL DEDUCTIONS")
            return False
        
        return True

    def fill_rows(self, board : Board, region_id_list, rows_to_fill):
        
        do_not_fill = []
        for region_id in region_id_list:
            do_not_fill.extend(board.region_dict[region_id])
        
        for row in rows_to_fill:
            for col in range(board.size):
                if (row,col) not in do_not_fill:
                    board.place_piece(row,col,-1)


    def fill_cols(self, board : Board, region_id_list, cols_to_fill):
        do_not_fill = []
        for region_id in region_id_list:
            do_not_fill.extend(board.region_dict[region_id])
        
        for col in cols_to_fill:
            for row in range(board.size):
                if (row,col) not in do_not_fill:
                    board.place_piece(row,col,-1)



    def n_regions_line_deduction(self, board:Board):
        prev_board = copy.deepcopy(board)


        row_dict = defaultdict(list)
        col_dict = defaultdict(list)

        for region_id, positions in board.region_dict.items():
            region_row = set()
            region_col = set()
            for row, col in positions:
                region_row.add(row)
                region_col.add(col)

            row_key = tuple(sorted(region_row))
            col_key = tuple(sorted(region_col))

            if row_key:
                row_dict[row_key].append(region_id)
            if col_key:
                col_dict[col_key].append(region_id)


        #print("Region Line Deduction")
        for row_list, region_id_list in row_dict.items():
            if len(row_list) == len(region_id_list):

                #print(f"Row: {row_list}: {region_id_list}")
                self.fill_rows(board,region_id_list,list(row_list))
        
        #print()
        for col_list, region_id_list in col_dict.items():
            if len(col_list) == len(region_id_list):
                #print(f"Column: {col_list}: {region_id_list}")
                self.fill_cols(board,region_id_list,list(col_list))

        #print()
        if board.pieces == prev_board.pieces:
            print("NO FURTHER n REGION DEDUCTIONS")
            return False
        
        return True
    
    def place_last_piece(self, board : Board):

        fill_queens = []

        for region_id in board.region_dict:

            empty_cells = board.region_dict[region_id]

            if len(empty_cells) == 1:
                fill_queens.append(empty_cells[0])

        if fill_queens:
            for cell in fill_queens:
                board.queen_autofill(cell[0],cell[1])

    def reduce_board_state(self, board):
        # Start by running both functions
        while True:
            # Copy the current state to check for changes
            previous_state = copy.deepcopy(board)

            # Run both functions on the board
            func1_changed = self.internal_overlap(board)  # Run first function
            func2_changed = self.n_regions_line_deduction(board)  # Run second function
            func3_changed = self.row_col_overlap(board)


            self.place_last_piece(board)


            # If neither function caused a change in the board state, stop
            if not func1_changed and not func2_changed and not func3_changed:
                break  # No change, exit the loop


            # Otherwise, continue with the new state
            if board == previous_state:
                break  # If the state hasn't changed, break the loop

        return


            