from flask import Flask,request,jsonify
from flask_cors import CORS
from api import api # api.py에서 함수를 import
import os
import threading
from google_authorize import google_authorize
from pymongo import MongoClient


app = Flask(__name__)
CORS(app)  

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
    user_info = request.json
    if not user_info:
        print("사용자 정보가 비어있습니다.")
        return "사용자 정보가 비어있습니다.", 400
    email = user_info.get('email')
    name = user_info.get('name')
    detail = user_info.get('detail')
    print(user_info)
    # joinUser(name, email, detail)
    MONGO_URI = "mongodb+srv://hayeon:yho39064475@monoletter.3xsxz4k.mongodb.net/?retryWrites=true&w=majority&appName=monoletter"
    client = MongoClient(MONGO_URI)
    db = client.monoletter
    user = {'name':name, 'email':email, 'detail' : detail}
    existing_user = db.users.find_one({'email': email})

    if existing_user is None:
        # 새로운 사용자 등록
        user = {'name': name, 'email': email, 'detail': detail}
        db.users.insert_one(user)
        response = {
            'status': 'New user',
            'message': 'Registration complete.'
        }
    else:
        # 이미 가입된 사용자
        response = {
            'status': 'Joined user',
            'message': 'Email is already registered.'
        }

    return jsonify(response)


    





# def joinUser(name, email, detail):
#     MONGO_URI = "mongodb+srv://hayeon:yho39064475@monoletter.3xsxz4k.mongodb.net/?retryWrites=true&w=majority&appName=monoletter"
#     client = MongoClient(MONGO_URI)
#     db = client.monoletter
#     user = {'name':name, 'email':email, 'detail' : detail}
#     db.users.insert_one(user)
#     return True

    
    
if __name__ == '__main__':
    app.run(host="0.0.0.0", port="5000", debug=True)