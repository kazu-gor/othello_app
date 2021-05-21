import numpy as np

def edit_value(value):
    try:
        value = value.replace(" ", "").replace("[[", "")\
            .replace("]]", "").replace("[", "").replace("]", "")
        board = np.fromstring(value, dtype="int32", sep=",").reshape(8 ,8)
    except Exception as e:
        return e.message

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