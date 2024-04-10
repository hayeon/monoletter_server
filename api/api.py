from flask import Flask, request, jsonify
from flask_cors import CORS

api = Flask(__name__)
api.config['DEBUG'] = True
CORS(api)


@api.route('/data', methods=['POST'])
def receive_string():
    data = request.json
    received_string = data['string']
    print("데이터 도착!", received_string)
    return jsonify({"response": received_string})

if __name__ == '__main__':
    api.run(host="0.0.0.0", port="5000",  debug=True)