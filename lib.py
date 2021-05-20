import numpy as np

def edit_value(value):
    value = value.split(" ")
    print(value)
    array_list = []
    for i in value:
        print(i)
        try:
            array_list.append(int(i))
        except ValueError:
            pass
    board = np.array(array_list)
    print(board)
    try:
        board = board.reshape(8, 8)
    except ValueError:
        return None
    return board
    
    
if __name__ == '__main__':
    input = """\
    [[ 0,  0,  0,  0,  0,  0,  0,  0],
    [ 0,  0,  0,  0,  0,  0,  0,  0],
    [ 0,  0,  0,  0,  0,  0,  0,  0],
    [ 0,  0,  0,  1, -1,  0,  0,  0],
    [ 0,  0,  0, -1,  1,  0,  0,  0],
    [ 0,  0,  0,  0,  0,  0,  0,  0],
    [ 0,  0,  0,  0,  0,  0,  0,  0],
    [ 0,  0,  0,  0,  0,  0,  0,  0]]"""
    board = edit_value(input)
    print(board)