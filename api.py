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