from copy import deepcopy
from collections import defaultdict
class Board:
    def __init__(self, name, size, region_map):
        self.name = name
        self.size = size
        self.region_map = region_map # Color / region ids

        self.queens = set()
        self.markers = set()

        self.regions_dict = self.set_region_dict()

    
    def set_region_dict(self):
        """Creates and returns a dictionary mapping region IDs to their (row, col) coordinates."""
        region_dict = defaultdict(set)

        for row in range(self.size):
            for col in range(self.size):
                region_id = self.region_map[row][col]
                region_dict[region_id].add((row, col))

        return region_dict 
    
    def copy_pieces(self):
        queens_copy = deepcopy(self.queens)
        markers_copy = deepcopy(self.markers)

        return (queens_copy, markers_copy)
    
    def copy(self, new_state):
        self.queens = deepcopy(new_state.queens)
        self.markers = deepcopy(new_state.markers)
        
    def reset_board(self):
        self.queens = set()
        self.markers = set()
        
    def is_empty(self):
        if not self.queens and not self.markers:
            return True
        return False
        
    def cell_is_queen(self, row, col):
        return (row, col) in self.queens
    
    def cell_is_marker(self, row, col):
        return (row, col) in self.markers
    
    def cell_is_empty(self, row, col):
        if not self.cell_is_queen(row, col) and not self.cell_is_marker(row, col):
            return True
        return False
    
        
    def place_queen(self, row, col):
        if 0 <= row < self.size and 0 <= col < self.size:
            self.queens.add((row,col))

    def remove_queen(self, row, col):
        if 0 <= row < self.size and 0 <= col < self.size:
            self.queens.discard((row,col))

    def place_marker(self, row, col):
        if 0 <= row < self.size and 0 <= col < self.size:
            self.markers.add((row,col))

    def remove_marker(self, row, col):
        if 0 <= row < self.size and 0 <= col < self.size:
            self.markers.discard((row,col))

    def player_autofill_queen(self, queen_row, queen_col):


        
        # Optionally get the region ID if needed (not used in this code)
        region_id = self.region_map[queen_row][queen_col]
        
        # Remove the queen from its current position.
        self.remove_queen(queen_row, queen_col)
        
        # Process the queen's column: For every row except queen_row,
        # remove any queen (if present) and place a marker.
        for row in range(self.size):
            if row != queen_row:
                self.remove_queen(row, queen_col)  # Unconditionally remove any queen
                self.place_marker(row, queen_col)  # Place marker in this cell
        
        # Process the queen's row: For every column except queen_col,
        # remove any queen (if present) and place a marker.
        for col in range(self.size):
            if col != queen_col:
                self.remove_queen(queen_row, col)
                self.place_marker(queen_row, col)

        for r_offset, c_offset in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:

            n_row = queen_row + r_offset
            n_col = queen_col + c_offset

            self.remove_queen(n_row, n_col)
            self.place_marker(n_row, n_col)

        for row, col in self.regions_dict[region_id]:
            self.remove_queen(row,col)
            self.place_marker(row,col)
        
        # Remove any marker from the queen's original cell,
        # then place the queen back in that position.
        self.remove_marker(queen_row, queen_col)
        self.place_queen(queen_row, queen_col)


    # Assume that we never wipe a previous queen or marker
    def algo_autofill_queen(self, queen_row, queen_col):
        self.place_queen(queen_row, queen_col)
        
        # new_markers = set()

        region_id = self.region_map[queen_row][queen_col]

        for row in range(self.size):
            if (row, queen_col) in self.markers or row == queen_row:
                continue

            # new_markers.add((row, queen_col))
            self.place_marker(row, queen_col)

        for col in range(self.size):
            if (queen_row, col) in self.markers or col == queen_col:
                continue

            # new_markers.add((queen_row, col))
            self.place_marker(queen_row, col)

        for r_offset, c_offset in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:

            n_row = queen_row + r_offset
            n_col = queen_col + c_offset

            if (n_row, n_col) in self.markers: continue

            self.place_marker(n_row, n_col)

            # if 0 <= n_row < self.size and 0 <= n_col < self.size:
            #     new_markers.add((n_row, n_col))

        for row, col in self.regions_dict[region_id]:
            if (row, col) in self.markers: continue
            if row == queen_row and col == queen_col: continue

            self.place_marker(row, col)
            # new_markers.add((row,col))


        # return new_markers

    def hypothetical_autofill(self, queen_row, queen_col):
        hyp_markers = set()

         # Optionally get the region ID if needed (not used in this code)
        region_id = self.region_map[queen_row][queen_col]
        
       
        # Process the queen's column: For every row except queen_row,
        # remove any queen (if present) and place a marker.
        for row in range(self.size):
            if row != queen_row:
                hyp_markers.add((row, queen_col))  # Place marker in this cell
        
        # Process the queen's row: For every column except queen_col,
        # remove any queen (if present) and place a marker.
        for col in range(self.size):
            if col != queen_col:
                hyp_markers.add((queen_row, col))

        for r_offset, c_offset in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:

            n_row = queen_row + r_offset
            n_col = queen_col + c_offset

            if 0 <= n_row < self.size and 0 <= n_col < self.size:
                hyp_markers.add((n_row,n_col))

        for row, col in self.regions_dict[region_id]:
            if row == queen_row and col == queen_col:
                continue
            hyp_markers.add((row,col))
        
        return hyp_markers