import json

class Board:
    def __init__(self, name, size, regions):
        self._name = name
        self._size = size
        self._regions = regions

#         self.pieces = [
#     [1, -1, 1, -1, 1],
#     [-1, 1, -1, 1, -1],
#     [1, -1, 1, -1, 1],
#     [-1, 1, -1, 1, -1],
#     [1, -1, 1, -1, 1]
# ]
        
        self.pieces = [[0 for _ in range(size)] for _ in range(size)]
        

    # Getter and Setter for 'name'
    def get_name(self):
        return self._name

    def set_name(self, name):
        self._name = name

    # Getter and Setter for 'size'
    def get_size(self):
        return self._size

    def set_size(self, size):
        self._size = size

    # Getter and Setter for 'regions'
    def get_regions(self):
        return self._regions

    def set_regions(self, regions):
        self._regions = regions

    def modify_piece(self, row, col, val):
        if 0 <= row < self.size and 0 <= col < self.size:
            self.pieces[row][col] = val
        else:
            print("Invalid position")