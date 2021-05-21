import requests
import pprint
import json

url = "http://127.0.0.1:5000/"
# url = "https://othelloapi.df.r.appspot.com"

value = """\
    [[ 0,  0,  0,  0,  0,  0,  0,  0],
    [ 0,  0,  0,  0,  0,  0,  0,  0],
    [ 0,  0,  0,  0,  0,  0,  0,  0],
    [ 0,  0,  0,  1, -1,  0,  0,  0],
    [ 0,  0,  0, -1,  1,  0,  0,  0],
    [ 0,  0,  0,  0,  0,  0,  0,  0],
    [ 0,  0,  0,  0,  0,  0,  0,  0],
    [ 0,  0,  0,  0,  0,  0,  0,  0]]"""

response = requests.post(url, {"board": value})

print(response)
pprint.pprint(response.json())
# json_lines = [ json.loads(s) for s in response if s != "" ]
# print(json_lines)