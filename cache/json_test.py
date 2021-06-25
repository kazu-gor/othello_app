import json
import numpy as np

json_open = open("othello_board.json", "r")
json_load = json.load(json_open)

# print(json_load)

board = list()

for num, lines in json_load["body"]["board"].items():
    print(lines)
    board.append(lines)

np_board = np.ndarray(board).reshape(8, -1)
print(np_board)
    
    