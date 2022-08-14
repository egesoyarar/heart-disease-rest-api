from flask import Flask

from model import model_build

app = Flask(__name__)

@app.route('/')
def hello_world():
    return model_build()


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)