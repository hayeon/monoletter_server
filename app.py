# app.py
from flask import Flask
import threading
import os
from api.api import api


app = Flask(__name__)
app.register_blueprint(api, url_prefix='/api')  # Blueprint 등록
def run_scrapy():
    os.chdir('jobkorea')
    os.system('scrapy crawl test')

@app.route('/')
def hello_world():
    threading.Thread(target=run_scrapy).start()
    print('Scrapy 스크립트 실행 중!')

if __name__ == '__main__':
    app.run(debug=True)
