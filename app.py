# from flask import Flask, request, jsonify
# from flask_cors import CORS

# api = Flask(__name__)
# api.config['DEBUG'] = True
# CORS(api)


# @api.route('/data', methods=['POST'])
# def receive_string():
#     data = request.json
#     received_string = data['string']
#     print("데이터 도착!", received_string)
#     return jsonify({"response": received_string})

# if __name__ == '__main__':
#     api.run(host="0.0.0.0", port="5000",  debug=True)
    


from flask import Flask
from flask_cors import CORS
from api.api import api 
import os
import threading

app = Flask(__name__)
CORS(app)  

app.register_blueprint(api, url_prefix='/data')  #컴포넌트 분리
@app.route('/')

def run_scrapy():
    os.chdir('jobkorea')
    os.system('scrapy crawl test')



def hello_world():
    threading.Thread(target=run_scrapy).start()
    print('Scrapy 스크립트 실행 중!')
    return 'Scrapy 스크립트가 실행되었습니다!', 200

if __name__ == '__main__':
    app.run(host="0.0.0.0", port="5000", debug=True)