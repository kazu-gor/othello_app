# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START gae_python38_app]
# [START gae_python3_app]

from flask import Flask, jsonify, abort, make_response
# import peewee

# class User(peewee.Model):
#     user_input = peewee.IntegerField()
    
api = Flask(__name__)

# @api.route('/', methods=['GET'])
# @api.route('/')
# def get_user():
#     try:
#         sum
#     except NameError:
#         sum = 0
#     try:
#         sum += 3
#     except User.DoesNotExist:
#         abort(404)
        
#     result = {
#         "data": {
#             "output": sum,
#         }
#     }
#     # return make_response(jsonify(result))
#     return result

# @api.errorhandler(404)
# def not_found(error):
#     # return make_response(jsonify({'error': 'Not found'}), 404)
#     return {'error': 'Not found'}
@api.route('/')
def hello():
    return 'Hello World'

if __name__ == '__main__':
    api.run(host='127.0.0.1', port=8080, debug=True)
    
# [END gae_python3_app]
# [END gae_python38_app]