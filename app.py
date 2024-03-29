from flask import Flask

app = Flask(__name__)

@app.route('/') #기존 경로 
def hello():
    return 'Hello, My First Flask!'

if __name__ == '__main__':
    app.run()