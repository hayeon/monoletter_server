from flask import Flask
from flask_cors import CORS
from api import api # api.py에서 함수를 import
import os
import threading


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
app.add_url_rule('/googlelogin', view_func=api.receive_code, methods=['POST'])


if __name__ == '__main__':
    app.run(host="0.0.0.0", port="5000", debug=True)