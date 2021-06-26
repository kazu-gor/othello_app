import json
import numpy as np

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

json_in = {
    "body": {'board': value}
}


# print(json_open)
# json_load = json.load(json_open)

board = list()
for num, lines in json_in["body"]["board"].items():
    print(lines)
    board.append(lines.replace("[", "").replace("]", "").split(","))

np_board = np.array(board).reshape(8, -1)
print(np_board.astype(("int8")))
print(np_board.shape)
    
    