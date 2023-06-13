# # server.py
# from flask import Flask, request, jsonify
#
# app = Flask(__name__)
#
# @app.route('/get_string', methods=['GET'])
# def get_string():
#     return jsonify({'message': 'Hello I love big booty gfs, this is your string!'}), 200
#
# @app.route('/post_string', methods=['POST'])
# def post_string():
#     data = request.get_json()
#     if 'message' in data:
#         return jsonify({'message': 'Received the string: {}'.format(data['message'])}), 200
#     else:
#         return jsonify({'error': 'No message provided.'}), 400
#
# if __name__ == "__main__":
#     app.run(port=5000)
# server.py
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/get_string', methods=['GET'])
def get_string():
    return jsonify({'message': 'Hello, this is your string!'}), 200

@app.route('/post_string', methods=['POST'])
def post_string():
    data = request.get_json()
    if 'message' in data:
        modified_string = '{} fives'.format(data['message'])
        return jsonify({'message': modified_string}), 200
    else:
        return jsonify({'error': 'No message provided.'}), 400

if __name__ == "__main__":
    app.run(port=5000)
