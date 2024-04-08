from flask import Blueprint, request, jsonify

api = Blueprint('api', __name__)

@api.route('/data', methods=['POST'])
def receive_data():
    data = request.json
    print(data)  # 받은 데이터
    return jsonify({'message': '데이터 성공!!', 'Data': data})
