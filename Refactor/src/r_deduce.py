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

            regional_overlaps = set.intersection(*regional_overlaps)

            # print(f"Region {region_id}: {regional_overlaps}")
           
            overlaps = overlaps.union(regional_overlaps)

        overlaps = overlaps - board.queens
        for (row, col) in overlaps:
            board.place_marker(row, col)


        return
        


    def reduce_board(self, board : Board):

        start = time.time()
        self.internal_overlap(board)
        elapsed = time.time() - start
        print(f"Deduction took {elapsed:.4f} seconds")

        return