import json

class Board:
    def __init__(self, name, size, regions):
        self.name = name
        self.size = size
        self.regions = regions

#         self.pieces = [
#     [1, -1, 1, -1, 1],
#     [-1, 1, -1, 1, -1],
#     [1, -1, 1, -1, 1],
#     [-1, 1, -1, 1, -1],
#     [1, -1, 1, -1, 1]
# ]
        
        self.pieces = [[0 for _ in range(size)] for _ in range(size)]
        


    def modify_piece(self, row, col, val):
        if 0 <= row < self.size and 0 <= col < self.size:

            # Toggle piece
            if self.pieces[row][col] == val:
                self.pieces[row][col] = 0

            else:
                self.pieces[row][col] = val
        else:
            print("Invalid position")