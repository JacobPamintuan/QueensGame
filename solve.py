from board import Board
from validate import Validator
import copy
import pdb

class Solver:
    def __init__(self,validator : Validator):
        self.validator = validator
        self.num_seeds = 0

    def brute_force_helper(self, board_data : Board,screen):

        # board_data.draw_board(screen)
        

        if self.validator.validate_win(board_data):
            return True
        
        for row in range(board_data.size):
            for col in range(board_data.size):
                if board_data.pieces[row][col] == 0:

                    temp_pieces = copy.deepcopy(board_data.pieces)

                    board_data.queen_autofill(row,col)

                    
                    if self.brute_force_helper(board_data, screen):
                        return True
                    
                    else:
                        board_data.pieces = copy.deepcopy(temp_pieces)
                        # board_data.draw_board(screen, False)

                        board_data.algo_modify_piece(row,col,-1)
                        return self.brute_force_helper(board_data,screen)
                        board_data.draw_board(screen, False)

                    # board_data.draw_board(screen, False)

        # board_data.draw_board(screen, False)
        return False

        # board_data.queen_autofill(1,1)

    def brute_force(self, board_data : Board,screen):

        self.num_seeds = 0

        print("BRUTE FORCE")
        
        original = copy.deepcopy(board_data)
        
        
        for row in range(board_data.size):
            for col in range(board_data.size):
                
                if board_data.pieces[row][col] == 0:

                    print(f"ATTEMPTING SEED: [{row}][{col}]")
                    self.num_seeds += 1

                    # if row == 0 and col == 3:
                    #     pdb.set_trace()

                    temp = copy.deepcopy(board_data)
                    
                    temp.queen_autofill(row,col)

                    # temp.draw_board(screen, False)


                    attempt = self.brute_force_helper(temp,screen)

                    # temp.draw_board(screen, False)


                    if attempt:
                        board_data = copy.deepcopy(temp)

                        return board_data
                
        print("No Solution found")
        return original
    
    def brute_force_optimal_seed(self, board_data : Board, screen):

        self.num_seeds = 0

        print("BRUTE FORCE OPTIMAL SEED")

        original = copy.deepcopy(board_data)
        

        smalleset_region_id = min(board_data.region_dict, key=lambda k: len(board_data.region_dict[k]))

        for seed in board_data.region_dict[smalleset_region_id]:


            row, col = seed

            if board_data.pieces[row][col] == 0 or board_data.pieces[row][col] == 1:

                print(f"ATTEMPTING SEED: [{row}][{col}]")
                self.num_seeds += 1


                temp = copy.deepcopy(board_data)

                temp.queen_autofill(row, col)

                attempt = self.brute_force_helper(temp,screen)

                if attempt:
                    board_data = copy.deepcopy(temp)

                    return board_data
                
        print("No Solution found")
        return original


        

