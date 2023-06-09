from flask import Flask
from flask import request
import os

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route("/test", methods=['POST'])
def test():
    file = request.files['file']
    filename = file.filename
    file.save(os.path.join("files", filename))
    return {"result": "ok"}


if __name__ == '__main__':
    app.run()
