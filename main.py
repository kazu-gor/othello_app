
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

import numpy as np
from flask import *
import nevergrad

from muzero_general import muzero
from lib.edit import edit_value
    
app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def othello():
    if request.method == "GET":
        try:
            return json.dumps({"result": 1})
        except Exception:
            return abort(400)
    if request.method == 'POST':
        try:
            model = muzero.MuZero("othello_update")
            board = edit_value(request.get_json(force=True))
            # board_player1 = np.where(board == 1, 1.0, 0.0)
            # board_player2 = np.where(board == -1, 1.0, 0.0)
            # board_to_play = np.full((8, 8), 1, dtype="int32")
            # observation = np.array([board_player1, board_player2, board_to_play])
            # row, col = model.application_match(render=False, board=board, observation=observation)
            # return json.dumps({"result": str(row) + "," + str(col)})
            return json.dumps({"result": request.get_json(force=True)})
        except Exception:
            return abort(400)
    else:
        return abort(400)


@app.errorhandler(404)
def not_found(error):
    # return make_response(jsonify({'error': 'Not found'}), 404)
    return {'error': 'Not found'}

if __name__ == '__main__':
    app.run(debug=True, host="127.0.0.1")
# [END gae_python3_app]
# [END gae_python38_app]