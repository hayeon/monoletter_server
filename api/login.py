from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token
import requests

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'a123eoe891234'
jwt = JWTManager(app)

@app.route('/authorize', methods=['POST'])

def google_authorize():
    auth_code = request.json.get('authCode')
    # Google OAuth 2.0 엔드포인트를 사용하여 액세스 토큰 얻기
    token_data = {
        'code': auth_code,
        'client_id': 'CLIENT_ID',
        'client_secret': 'CLIENT_SECRET',
        'redirect_uri': 'postmessage',
        'grant_type': 'authorization_code',
    }
    token_response = requests.post('https://oauth2.googleapis.com/token', data=token_data)
    token_info = token_response.json()
    access_token = token_info.get('access_token')

    # 액세스 토큰을 사용하여 사용자 정보 얻기
    userinfo_response = requests.get(
        'https://www.googleapis.com/oauth2/v3/userinfo',
        params={'access_token': access_token}
    )
    userinfo = userinfo_response.json()

   #데이터베이스에 저장

    # JWT 토큰 발급
    jwt_token = create_access_token(identity=userinfo['email'])

    return jsonify(jwt_token=jwt_token), 200

if __name__ == '__main__':
    app.run(debug=True)
