from board import Board
from validate import validate_move, validate_win
import copy
import pdb

def brute_force_helper(board_data : Board,screen):

    # board_data.draw_board(screen)
    

    if validate_win(board_data):
        return True
    
    for row in range(board_data.size):
        for col in range(board_data.size):
            if board_data.pieces[row][col] == 0:

                temp_pieces = copy.deepcopy(board_data.pieces)

                board_data.queen_autofill(row,col)

                
                if brute_force_helper(board_data, screen):
                    return True
                
                else:
                    board_data.pieces = copy.deepcopy(temp_pieces)
                    # board_data.draw_board(screen, False)

                    board_data.algo_modify_piece(row,col,-1)
                    return brute_force_helper(board_data,screen)
                    board_data.draw_board(screen, False)

                # board_data.draw_board(screen, False)

    # board_data.draw_board(screen, False)
    return False

    # board_data.queen_autofill(1,1)

def brute_force(board_data : Board,screen):
    
    original = copy.deepcopy(board_data)
    
    for row in range(board_data.size):
        for col in range(board_data.size):
            
            if board_data.pieces[row][col] == 0:

                print(f"[{row}][{col}]")

                # if row == 0 and col == 3:
                #     pdb.set_trace()

                temp = copy.deepcopy(board_data)
                
                temp.queen_autofill(row,col)

                # temp.draw_board(screen, False)


                attempt = brute_force_helper(temp,screen)

                # temp.draw_board(screen, False)


                if attempt:
                    board_data = copy.deepcopy(temp)

                    return board_data
            
    print("No Solution found")
    return original