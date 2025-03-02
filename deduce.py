from board import Board
import copy 
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

    def determine_overlap(self, board : Board, region_id):
        test_board = copy.deepcopy(board)
        # test_board.reset_board()

        X_positions = []
        for cell in board.region_dict[region_id]:
            test_board.queen_autofill(cell[0],cell[1])

            X_positions.append(self.get_X_positions(test_board))
            test_board = copy.deepcopy(board)

        common_coords = set.intersection(*X_positions)
        print(f"{region_id}: {common_coords}")
        return common_coords


    def all_overlap(self, board :Board):
        overlap = []

        prev_board = copy.deepcopy(board)

        for region_id in board.region_dict.keys():
            common_coords = self.determine_overlap(board, region_id)

            if common_coords:
                overlap.append(common_coords)

        for coord_sets in overlap:
            for row, col in coord_sets:
                board.place_piece(row,col,-1)

        if board == prev_board:
            print("NO FURTHER DEDUCTIONS")

        # print(overlap)
        # return overlap