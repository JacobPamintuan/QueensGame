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
    