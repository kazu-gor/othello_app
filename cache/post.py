import requests
import pprint
import json
import sys

if len(sys.argv) == 2:
    url = "http://127.0.0.1:5000/"
else:
    # url = "https://othelloapi.df.r.appspot.com"
    url = "https://clever-aleph-318009.an.r.appspot.com"
    # url = "https://test-api-312.df.r.appspot.com"

print("URL: ", url)

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

# input_json = json.dumps({'body': {'board': value}})
input_json = json.dumps({'board': value})
# print(input_json)

response = requests.post(url, input_json)
print(response)
try:
    print(response.json())
except Exception as e:
    pass

try:
    pprint.pprint(response.json())
except Exception as e:
    pass

# response = requests.post(url, {"error": value})
# print(response)
# try:
#     pprint.pprint(response.json())
# except Exception as e:
    # pass

# response = requests.get(url, {"board": value})
# print(response)
# try:
#     pprint.pprint(response.json())
# except Exception as e:
#     pass

# response = requests.get(url)
# print(response)
# try:
#     pprint.pprint(response.json())
# except Exception as e:
#     pass



# json_lines = [ json.loads(s) for s in response if s != "" ]
# print(json_lines)