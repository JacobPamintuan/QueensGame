from r_board import Board
import copy
from collections import defaultdict
import time

class Deducer:
    def __init__(self):
        pass

    def internal_overlap(self, board: Board):

        changed_board = False

        overlaps = set()

        for region_id, cells in board.regions_dict.items():
            available_cells = cells - board.queens - board.markers

            regional_overlaps = []

            for (row, col) in available_cells:
                regional_overlaps.append(board.hypothetical_autofill(row, col))
            if regional_overlaps:
                regional_overlaps = set.intersection(*regional_overlaps)

            # print(f"Region {region_id}: {regional_overlaps}")
            if regional_overlaps:
                overlaps = overlaps.union(regional_overlaps)

        overlaps = overlaps - board.queens

        if overlaps:
            for (row, col) in overlaps:
                board.place_marker(row, col)
            changed_board = True

        return changed_board
        return

    def row_col_overlap(self, board: Board):

        changed_board = False

        overlaps = set()

        for line in range(board.size):
            row_X_positions = []
            col_X_positions = []

            for col in range(board.size):
                if board.cell_is_empty(line, col):
                    row_X_positions.append(board.hypothetical_autofill(line,col))
            common_row_markers = set()
            if row_X_positions:
                common_row_markers = set.intersection(*row_X_positions)


            for row in range(board.size):
                if board.cell_is_empty(row,line):
                    col_X_positions.append(board.hypothetical_autofill(row, line))
            common_col_makers = set()
            if col_X_positions:
                common_col_makers = set.intersection(*col_X_positions)

            overlaps = overlaps | common_row_markers | common_col_makers
            
    
        overlaps = overlaps - board.queens

        if overlaps:
            for (row, col) in overlaps:
                board.place_marker(row, col)
            changed_board = True

        return changed_board

        return

    # "line" refers to either a row or col
    def exists_exclusively_in_window(self, board: Board, line_dict : defaultdict):
        
        # Key: tuple - window described by (start_line, end_line)
        # Value: list - list of region_ids in window 
        window_dict = defaultdict(list)

        for start_line in range(board.size):
            for end_line in range(start_line + 1, board.size):

                current_window = (start_line, end_line)
                regions_in_window = []

                for line_tuple, regions_list in line_dict.items():

                    if line_tuple[0] >= start_line and line_tuple[-1] <= end_line:
                        regions_in_window.extend(regions_list)

                if regions_in_window:

                    window_size = end_line - start_line + 1

                    if window_size == len(regions_in_window) and window_size != board.size:

                        window_dict[current_window] = regions_in_window

        

        return window_dict

    def sliding_window(self, board: Board):

        changed_board = False

        # Dictionary:
        # Key: tuple of row/col numbers
        # Value: List of region_ids that exist 
        # in that specific combination of row/cols
        row_dict = defaultdict(list)
        col_dict = defaultdict(list)


        for region_id, cells in board.regions_dict.items():
            region_row = set()
            region_col = set()

            for row, col in cells:

                # Different from OG, include queen pos
                if (row, col) not in board.markers:
                # if board.cell_is_empty(row,col):
                    region_row.add(row)
                    region_col.add(col)

            # Dict keys cant be sets
            row_key = tuple(sorted(region_row))
            col_key = tuple(sorted(region_col))

            if row_key:
                row_dict[row_key].append(region_id)
                col_dict[col_key].append(region_id)

        row_window_dict = self.exists_exclusively_in_window(board,row_dict)
        col_window_dict = self.exists_exclusively_in_window(board,col_dict)

        
    

        for window, region_ids in row_window_dict.items():
            start, end = window

            for row in range(start, end + 1):
                for col in range(board.size):
                    if board.cell_is_empty(row,col) and board.region_map[row][col] not in region_ids:
                        board.place_marker(row, col)
                        changed_board = True

        for window, region_ids in col_window_dict.items():
            start, end = window

            for col in range(start, end+1):
                for row in range(board.size):
                    if board.cell_is_empty(row,col) and board.region_map[row][col] not in region_ids:
                        board.place_marker(row, col)
                        changed_board = True

        return changed_board
        return

    def place_last_piece(self, board: Board):

        changed_board = False
        for region_id, cells in board.regions_dict.items():
            available_cells = cells - board.queens - board.markers

            if len(available_cells) == 1:
                changed_board = True
                last_cell = available_cells.pop()
                board.algo_autofill_queen(last_cell[0],last_cell[1])



        return changed_board

    def step_reduce_board(self, board : Board):


        a = self.internal_overlap(board)
        b = self.place_last_piece(board)

        c = self.row_col_overlap(board)
        d = self.place_last_piece(board)


        e = self.sliding_window(board)
        f = self.place_last_piece(board)





        changed = a | b | c | d | e | f

        return changed 
    
    def full_reduce_board(self, board: Board):


        while True:
            if not self.step_reduce_board(board):
                break

        
