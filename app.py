from flask import Flask,request,jsonify
from flask_cors import CORS
from api import api
import os
import threading
from pymongo import MongoClient
from bson.objectid import ObjectId
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), 'py-hanspell'))
from getKey import speller

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
       
        return jsonify(response)
    except PyMongoError as e:
        print(f"데이터베이스 오류 발생: {e}")
        return jsonify({'status': 500, 'message': 'Internal server error occurred.'}), 500
    except Exception as e:
        print(f"알 수 없는 오류 발생: {e}")
        return jsonify({'status': 500, 'message': 'An unexpected error occurred.'}), 500

#-------------------자소서 체크---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
@app.route('/lettercheck', methods=['POST'])
def get_letters():
    email = request.json.get('email')
    MONGO_URI = database_url
    client = MongoClient(MONGO_URI)
    db = client.monoletter
    
    if not email:
        return jsonify({'error': 'Missing email!'}), 400
    # 해당 이메일을 가진 사용자의 최근 자기소개서 찾기
    user = db.users.find_one({"email": email})
    userId = user['_id']
    # 가장 최근에 저장된 사용자의 letters 문서 찾기
    letters = db.letters.find_one({"userId": userId}, sort=[('_id', -1)])
    if not letters:
        return jsonify(False), 200
    else:
    # 자기소개서가 있으면 maintitle_id와 가장 마지막 subTitle_id 반환
    # subTitles 배열에서 가장 마지막 요소에 접근
        last_subTitle = letters['subTitles'][-1] if letters['subTitles'] else None
        last_subTitle_id = last_subTitle['subTitle_id'] if last_subTitle else None

    return jsonify({
        'mainTitle_id': str(letters['_id']),
        'subTitle_id': str(last_subTitle_id) if last_subTitle_id else None
    }), 200
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
@app.route('/addletter', methods=['POST'])
def add_letter():

    data = request.json
    email = data.get('email')
    mainTitle = data.get('mainTitle')
    
    if not email or not mainTitle:
        return jsonify({'status': 400, 'message': 'Missing required fields'}), 400
    
    MONGO_URI = database_url
    client = MongoClient(MONGO_URI)
    db = client.monoletter

    # 이메일 일치 사용자 확인
    user = db.users.find_one({"email": email})
    if not user:
        return jsonify({'status': 400, 'message': 'User not found'}), 400
    userId = user['_id']
    # 자기소개서 저장
    try:
        subTitle_id = ObjectId()
        letter_data = {
             "userId": userId,
            "mainTitle": mainTitle,
            "subTitles": [{
                "subTitle_id": subTitle_id,  # 각 subTitle에 대한 고유 ID 생성
                "subTitle": "",
                "letter": "",
                "feedback": ""
            }]
        }

        result = db.letters.insert_one(letter_data)
        mainTitle_id = result.inserted_id

        # ObjectId를 문자열로 변환하여 JSON 응답에 포함
        return jsonify({
            'status': 200,
            'message': 'Letter added successfully',
            'mainTitle_id': str(mainTitle_id),
            'subTitle_id': str(subTitle_id)
        }), 200
        
    except Exception as e:
        print(e)
        return jsonify({'status': 500, 'message': 'Internal server error occurred.'}), 500



@app.route('/loadletter', methods=['POST'])
def load_letter():
    data = request.json
    email = data.get('email') #접속한 유저정보 
    mainTitle_id = data.get('mainTitle_id')
    subTitle_id = data.get('subTitle_id')
    if not email or not mainTitle_id or not subTitle_id:
        return jsonify({'status': 400, 'message': 'Missing required fields'}), 400 #도착 데이터가 없을 때
    
    MONGO_URI = database_url
    client = MongoClient(MONGO_URI)
    db = client.monoletter

    # 이메일 일치 사용자 확인
    user = db.users.find_one({"email": email})
    if not user:
        return jsonify({'status': 400, 'message': 'User not found'}), 400 
    userId = user['_id']
    # 접속한 유저가 자기소개서를 작성한 유저와 같은지 확인 
    check = db.letters.find_one({"userId": ObjectId(userId), "_id": ObjectId(mainTitle_id)})

    # 이메일 일치 사용자 확인
    user = db.users.find_one({"email": email})
    if not user:
        return jsonify({'status': 400, 'message': 'User not found'}), 400 
    userId = user['_id']
    # 접속한 유저가 자기소개서를 작성한 유저와 같은지 확인 
    check = db.letters.find_one({"userId": ObjectId(userId), "_id": ObjectId(mainTitle_id)})
    if not check:
        return jsonify({'status': 400, 'message': '접근권한이 없는 사용자입니다.'}), 400

        # 자기소개서 로딩하기
    try:
        # 전체 문서를 가져와서 subTitles 배열을 탐색
        letter = db.letters.find_one({ "_id": ObjectId(mainTitle_id) })
        if not letter:
            return jsonify({'status': 400, 'message': 'Letter not found'}), 400

    # subTitles 배열에서 해당 subTitle_id 찾기
        subTitle = next((sub for sub in letter.get('subTitles', []) if sub.get('subTitle_id') == ObjectId(subTitle_id)), None)
        if not subTitle:
            return jsonify({'status': 400, 'message': 'SubTitle not found'}), 400

        # 찾은 subTitle 정보 반환
        return jsonify({
            'status': 200,
            'message': 'Letter loaded successfully',
            'subTitle': subTitle.get('subTitle', ''),
            'letter': subTitle.get('letter', ''),
            'feedback': subTitle.get('feedback', '')}), 200

    except Exception as e:
        print(e)
        return jsonify({'status': 500, 'message': 'Internal server error occurred.'}), 500
    
    #----------------------------------------모든 db 리턴하기-----------------------------------------------------------------
@app.route('/loadallletter', methods=['POST'])
def loadAll_letter():
    data = request.json
    email = data.get('email') #접속한 유저정보 
    mainTitle_id = data.get('mainTitle_id')

    if not email or not mainTitle_id:
        return jsonify({'status': 400, 'message': 'Missing required fields'}), 400 #도착 데이터가 없을 때
    
    MONGO_URI = database_url
    client = MongoClient(MONGO_URI)
    db = client.monoletter

    # 이메일 일치 사용자 확인
    user = db.users.find_one({"email": email})
    if not user:
        return jsonify({'status': 400, 'message': 'User not found'}), 400 
    userId = user['_id']
    # 접속한 유저가 자기소개서를 작성한 유저와 같은지 확인 
    check = db.letters.find_one({"userId": ObjectId(userId), "_id": ObjectId(mainTitle_id)})
    if not check:
        return jsonify({'status': 400, 'message': '접근권한이 없는 사용자입니다.'}), 400

    try:
        # 사용자 ID를 기반으로 모든 자소서 문서를 가져옴
        letters = list(db.letters.find({"userId": ObjectId(userId)}))
        letters_list = []
        # 각 자소서 문서에 대해 반복
        for letter in letters:
        # 각 자소서 문서의 subTitle 정보를 포함한 전체 정보를 리스트에 추가
            sub_titles = []
            for sub_title in letter.get("subTitles", []):
                sub_titles.append({
                    "subTitle_id": str(sub_title.get("subTitle_id", "")),  # ObjectId를 문자열로 변환
                    "subTitle": sub_title.get("subTitle", ""),
                    "letter": sub_title.get("letter", ""),
                    "feedback": sub_title.get("feedback", "")
            })
        
            letters_list.append({"mainTitle": letter.get("mainTitle", ""),"mainTitle_id": str(letter.get("_id", "")), "subTitles": sub_titles})


    # 모든 정보가 담긴 리스트를 반환
        return jsonify({
            'status': 200,
            'message': 'Letters loaded successfully',
            'letters': letters_list
        }), 200
    except Exception as e:
        print(e)
        return jsonify({'status': 500, 'message': 'Internal server error occurred.'}), 500



@app.route('/saveletter', methods=['POST'])
def save_letter():
    data = request.json
    print(data)
    email = data.get('email')
    mainTitle_id = data.get('mainTitle_id')
    subTitle_id = data.get('subTitle_id')
    letter = data.get('letter')
    feedback = data.get('feedback')
    subTitle = data.get('subTitle')
    
    if not email :
        return jsonify({'status': 400, 'message': '사용자 정보가 없습니다.'}), 400
    
      
    MONGO_URI = database_url
    client = MongoClient(MONGO_URI)
    db = client.monoletter
    # 이메일 일치 사용자 확인
    user = db.users.find_one({"email": email})
    if not user:
        return jsonify({'status': 400, 'message': '회원조회가 불가능한 유저입니다.'}), 400
    
    userid = user['_id']
    check = db.letters.find_one({"userId": ObjectId(userid), "_id": ObjectId(mainTitle_id)})
    if not check:
        return jsonify({'status': 400, 'message': '접근권한이 없는 사용자입니다.'}), 400
    # 자기소개서 저장
    try:
        # 사용자의 자기소개서에서 해당 subTitle_id를 찾아 letter와 feedback 업데이트
        result = db.letters.update_one(
         {"_id": ObjectId(mainTitle_id), 
          "subTitles.subTitle_id": ObjectId(subTitle_id)},
         {"$set": {
            "subTitles.$.letter": letter,
            "subTitles.$.feedback": feedback,
            "subTitles.$.subTitle": subTitle 
        }}
    )

        # 업데이트가 성공적으로 이루어졌는지 확인
        if result.matched_count == 0:
            return jsonify({'status': 400, 'message': '임시저장에 실패했습니다.'}), 400

        return jsonify({'status': 200, 'message': '성공적으로 저장했습니다.'}), 200
    except Exception as e:
        print(e)
        return jsonify({'status': 500, 'message': 'Internal server error occurred.'}), 500
    
    ##--------------------자기소개서 항목 추가하기-----------
@app.route('/addsubletter', methods=['POST'])
def add_subletter():
    data = request.json
    email = data.get('email')
    mainTitle_id = data.get('mainTitle_id')
    
    if not email or not mainTitle_id:
        return jsonify({'status': 400, 'message': 'Missing required fields'}), 400
    
    MONGO_URI = database_url
    client = MongoClient(MONGO_URI)
    db = client.monoletter

    # 이메일 일치 사용자 확인
    user = db.users.find_one({"email": email})
    if not user:
        return jsonify({'status': 400, 'message': 'User not found'}), 400
    userId = user['_id']

    # 접속한 유저가 자기소개서를 작성한 유저와 같은지 확인
    check = db.letters.find_one({"userId": ObjectId(userId), "_id": ObjectId(mainTitle_id)})
    if not check:
        return jsonify({'status': 400, 'message': '접근권한이 없는 사용자입니다.'}), 400
    # 자기소개서에 새로운 서브 타이틀 추가
    try:
        subTitle_id = ObjectId()
        new_subTitle = {
            "subTitle_id": subTitle_id,
            "subTitle": "",
            "letter": "",
            "feedback": ""
        }

        # 기존 문서에 새로운 서브 타이틀 추가
        result = db.letters.update_one(
            {"_id": ObjectId(mainTitle_id)},
            {"$push": {"subTitles": new_subTitle}}
        )

        if result.modified_count == 0:
            return jsonify({'status': 500, 'message': 'Failed to add new subTitle'}), 500

        return jsonify({
            'status': 200,
            'message': 'Letter added successfully',
            'mainTitle_id': str(mainTitle_id),
            'subTitle_id': str(subTitle_id)
        }), 200
        
    except Exception as e:
        print(e)
        return jsonify({'status': 500, 'message': 'Internal server error occurred.'}), 500

@app.route('/speller', methods=['POST'])
def check_spelling():
    letter = request.json.get('letter')
    res = speller(letter)
    try:
        response = {
            "original": str(res.original),
            "checked": str(res.checked),
            "errors": str(res.errors),
        }
        print(response)
        return jsonify(response)

    

    
    except Exception as e:
        print(e)
        return jsonify({'status': 500, 'message': 'Internal server error occurred.'}), 500



    
if __name__ == '__main__':
    app.run(host="0.0.0.0", port="5000", debug=True)