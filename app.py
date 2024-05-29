from flask import Flask,request,jsonify
from flask_cors import CORS
from api import api # api.py에서 함수를 import
import os
import threading
from pymongo import MongoClient
from pymongo.errors import PyMongoError

app = Flask(__name__)
CORS(app)  
database_url = os.getenv('MONGO_URI')
@app.route('/')


def run_scrapy():
    os.chdir('jobkorea')
    os.system('scrapy crawl test')

def hello_world():
    threading.Thread(target=run_scrapy).start()
    print('Scrapy 스크립트 실행 중!')
    return 'Scrapy 스크립트가 실행되었습니다!', 200

# api 통신
app.add_url_rule('/data', view_func=api.receive_letter, methods=['POST'])
@app.route('/googlelogin', methods=['POST'])
    #디비저장
def user_info():
    try:
        user_info = request.json
        if not user_info:
            print("사용자 정보가 비어있습니다.")
            return "사용자 정보가 비어있습니다.", 400
        email = user_info.get('email')
        name = user_info.get('name')
        detail = user_info.get('detail')
        print(user_info)
        MONGO_URI = database_url
        client = MongoClient(MONGO_URI)
        db = client.monoletter
        user = {'name': name, 'email': email, 'detail': detail}
        existing_user = db.users.find_one({'email': email})
        blinkUser = db.users.find_one({'detail': ""}) #회원가입은 했지만 상세정보를 입력하지 않은 유저
        if existing_user is None:
            # 새로운 사용자 등록
            db.users.insert_one(user)
            response = {
                'status': 200,
                'message': 'Registration complete.'
            }
        elif blinkUser: {
                'status': 200,
                'message': 'Please complete your profile details.'  
            } 
        else:
            # 이미 가입된 사용자
            response = {
                'status': 200,
                'message': 'Email is already registered.'
            }
       
        print(response)
        return jsonify(response)
    except PyMongoError as e:
        print(f"데이터베이스 오류 발생: {e}")
        return jsonify({'status': 500, 'message': 'Internal server error occurred.'}), 500
    except Exception as e:
        print(f"알 수 없는 오류 발생: {e}")
        return jsonify({'status': 500, 'message': 'An unexpected error occurred.'}), 500
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
@app.route('/updatedetail', methods=['PUT'])
def update_detail():
    # 클라이언트로부터 이메일과 새로운 detail을 받음
    user_info = request.json
    email = user_info.get('email')
    new_detail = user_info.get('detail')
    MONGO_URI = database_url
    client = MongoClient(MONGO_URI)
    db = client.monoletter
    
    # 이메일과 일치하는 사용자 찾기
    result = db.users.update_one(
        {"email": email},
        {"$set": {"detail": new_detail}}
    )
    
    # 업데이트 성공 여부에 따라 응답 반환
    if result.matched_count:
        print("detail을 db에 저장하였습니다")
        return jsonify({"msg": "Detail updated successfully"}), 200
    else:
        print("detail을 db에 저장하지 못했습니다")
        return jsonify({"msg": "User not found"}), 404

    #-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
@app.route('/add_letter', methods=['POST'])
def add_letter():
    data = request.json
    email = data.get('email')
    listTitle = data.get('listTitle')
    question = data.get('question')
    letter = data.get('letter ')
    feedback = data.get('feedback')
    
    if not email or not listTitle or not question or not letter or not feedback:
        return jsonify({'status': 400, 'message': 'Missing required fields'}), 400

    MONGO_URI = database_url
    client = MongoClient(MONGO_URI)
    db = client.monoletter

    # 이메일 일치 사용자
    user = db.users.find_one({"email": email})
    if not user:
        return jsonify({'status': 400, 'message': 'User not found'}), 400

    user_id = user['_id']

    letter_detail = {
        "question": question,
        "letter": letter,
        "feedback": feedback
    }

    # listTitle이 같은 문서를 찾아서 업데이트 또는 새로 삽입
    result = db.letters.update_one(
        {"user_id": user_id, "listTitle": listTitle},
        {"$push": {"details": letter_detail}},
        upsert=True
    )
    if result.matched_count:
        print("자소서를 db에 저장하였습니다")
        return jsonify({'status': 200, 'message': 'Letter added or updated successfully'}), 200
    else:
        print("자소서를 db에 저장하지 못했습니다")
        return jsonify({'status': 200, 'message': 'Letter added Fale'}), 500

if __name__ == '__main__':
    app.run(debug=True)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port="5000", debug=True)