
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

import peewee
import numpy as np
from flask import *

from muzero_general import muzero
from lib import edit_value

# class User(peewee.Model):
#     user_input = peewee.IntegerField()
    
app = Flask(__name__)

@app.route('/')
def index():
    html = '''
    <form action="/othello">
        <p><label>test: </label>
        <input type="text" name="board" value="default">
        <button type="submit" formmethod="get">GET</button>
        <button type="submit" formmethod="post">POST</button></p>
    </form>
    '''
    return Markup(html)

@app.route('/othello', methods=['GET', 'POST'])
def othello():
    if request.method == 'GET':
        return 0
    if request.method == 'POST':
        model = muzero.MuZero("othello_update")
        board = edit_value(request.form['board'])
        board_player1 = np.where(board == 1, 1.0, 0.0)
        board_player2 = np.where(board == -1, 1.0, 0.0)
        board_to_play = np.full((8, 8), 1, dtype="int32")
        observation = np.array([board_player1, board_player2, board_to_play])
        row, col = model.application_match(render=False, board=board, observation=observation)
        return {"result": str(row) + "," + str(col)}
    else:
        return abort(400)


@app.errorhandler(404)
def not_found(error):
    # return make_response(jsonify({'error': 'Not found'}), 404)
    return {'error': 'Not found'}

if __name__ == '__main__':
    app.run()
# [END gae_python3_app]
# [END gae_python38_app]