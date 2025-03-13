from r_board import Board
import copy
from collections import defaultdict
import time

class Deducer:
    def __init__(self):
        pass

    def internal_overlap(self, board: Board):

        overlaps = set()

        for region_id, cells in board.region_dict.items():
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
        for (row, col) in overlaps:
            board.place_marker(row, col)


        return
    

    def row_col_overlap(self, board: Board):
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

        for (row, col) in overlaps:
            board.place_marker(row, col)


        return


    def reduce_board(self, board : Board):

        start = time.time()
        self.internal_overlap(board)
        self.row_col_overlap(board)
        elapsed = time.time() - start
        print(f"Deduction took {elapsed:.4f} seconds")

        return