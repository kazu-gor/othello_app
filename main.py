
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

from flask import *
import peewee

from muzero_general import muzero

# class User(peewee.Model):
#     user_input = peewee.IntegerField()
    
app = Flask(__name__)

@app.route('/')
def index():
    html = '''
    <form action="/othello">
        <p><label>input:[row, col] </label>
        <input type="text" name="index" value="0,1">
        <button type="submit" formethod="get">GET</button>
        <button type="submit" formethod="post">POST</button></p>
    </form>
    '''
    return Markup(html)

@app.route('/othello', methods=['GET', 'POST'])
def othello():
    try:
        if request.method == 'GET':
            return request.args.get('index', '')
        elif request.method == 'POST':
            return request.form['index']
        else:
            return abort(400)
    except Exception as e:
        return str(e)
    

# @app.errorhandler(404)
# def not_found(error):
#     # return make_response(jsonify({'error': 'Not found'}), 404)
#     return {'error': 'Not found'}

if __name__ == '__main__':
    app.run()
# [END gae_python3_app]
# [END gae_python38_app]