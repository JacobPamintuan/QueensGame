from board import Board
from validate import Validator
import copy


class Solver:
    def __init__(self,validator : Validator):
        self.validator = validator
        self.num_seeds = 0
        self.chosen_seed = (-1,-1)

    def brute_force_helper(self, board_data : Board):

  
        

        if self.validator.validate_win(board_data):
            return True
        
        for row in range(board_data.size):
            for col in range(board_data.size):
                if board_data.pieces[row][col] == 0:

                    temp_pieces = copy.deepcopy(board_data.pieces)

                    board_data.queen_autofill(row,col)

                    
                    if self.brute_force_helper(board_data):
                        return True
                    
                    else:
                        board_data.pieces = copy.deepcopy(temp_pieces)


                        board_data.place_piece(row,col,-1)
                        return self.brute_force_helper(board_data)




        return False

        # board_data.queen_autofill(1,1)

    def brute_force(self, board_data : Board):

        self.num_seeds = 0

        print("BRUTE FORCE")
        
        original = copy.deepcopy(board_data)
        
        
        for row in range(board_data.size):
            for col in range(board_data.size):
                
                if board_data.pieces[row][col] == 0:

                    print(f"ATTEMPTING SEED: [{row}][{col}]")
                    self.num_seeds += 1



                    temp = copy.deepcopy(board_data)
                    
                    temp.queen_autofill(row,col)

                    attempt = self.brute_force_helper(temp)



                    if attempt:
                        board_data = copy.deepcopy(temp)

                        self.chosen_seed = (row,col)

                        return board_data
                
        print("No Solution found")
        return original
    
    def brute_force_optimal_seed(self, board_data : Board):

        self.num_seeds = 0

        print("BRUTE FORCE OPTIMAL SEED")

        original = copy.deepcopy(board_data)
        
        if board_data.region_dict:
            smalleset_region_id = min(board_data.region_dict, key=lambda k: len(board_data.region_dict[k]))
        else: return board_data

        for seed in board_data.region_dict[smalleset_region_id]:


            row, col = seed

            if board_data.pieces[row][col] == 0 or board_data.pieces[row][col] == 1:

                print(f"ATTEMPTING SEED: [{row}][{col}]")
                self.num_seeds += 1


                temp = copy.deepcopy(board_data)

                temp.queen_autofill(row, col)

                attempt = self.brute_force_helper(temp)

                if attempt:
                    board_data = copy.deepcopy(temp)
                    self.chosen_seed = seed
                

                    return board_data
                
        print("No Solution found")
        return original


        

