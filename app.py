# app.py
from flask import Flask
import threading
import os

app = Flask(__name__)

def run_scrapy():
    # Scrapy 프로젝트의 위치로 이동
    os.chdir('jobkorea')
    # Scrapy 스크립트 실행
    os.system('scrapy crawl test')

@app.route('/')
def hello_world():
    # 별도의 스레드에서 Scrapy 스크립트 실행
    threading.Thread(target=run_scrapy).start()
    return 'Scrapy 스크립트 실행 중!'

if __name__ == '__main__':
    app.run(debug=True)
