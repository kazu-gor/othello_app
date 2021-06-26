import numpy as np
import json

def  edit_value(value):
    try:
        board_list = list()
        
        for _, lines in value["board"].items():
            board_list.append(lines.replace("[", "").replace("]", "").replace("\n", "").split(","))
        np_board = np.array(board_list).astype("int32").reshape(8, 8)
        
    except Exception:
        return 0
    return np_board
        
    
    
if __name__ == '__main__':
    
    value = {
    '0': '[0,0,0,0,0,0,0,0]',
    '1': '[0,0,0,0,0,0,0,0]',
    '2': '[0,0,0,0,0,0,0,0]',
    '3': '[0,0,0,-1,1,0,0,0]',
    '4': '[0,0,0,1,-1,0,0,0]',
    '5': '[0,0,0,0,0,0,0,0]',
    '6': '[0,0,0,0,0,0,0,0]',
    '7': '[0,0,0,0,0,0,0,0]',
    }

    json_in = {'board': value}
    
    print(json_in)
    board = edit_value(json_in)
    print(board)
    print(type(board))
    print(board.shape)