class Board:
    def __init__(self, name, size, region_map):
        self.name = name
        self.size = size
        self.region_map = region_map # Color / region ids

        self.queens = set()
        self.markers = set()

        self.region_dict = self.set_region_dict()

    def set_region_dict(self):
        """Creates and returns a dictionary mapping region IDs to their (row, col) coordinates."""
        region_dict = {}  # Initialize an empty dictionary

        for row in range(self.size):
            for col in range(self.size):
                region_id = self.region_map[row][col]
                region_dict.setdefault(region_id, []).append((row, col))  # Correct usage

        return region_dict  # Return the constructed dictionary
        
    def reset_board(self):
        self.queens = set()
        self.markers = set()
        
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

    def autofill_queen(self, queen_row, queen_col):
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
            self.place_marker(queen_row + r_offset, queen_col + c_offset)
        
        # Remove any marker from the queen's original cell,
        # then place the queen back in that position.
        self.remove_marker(queen_row, queen_col)
        self.place_queen(queen_row, queen_col)

            
    