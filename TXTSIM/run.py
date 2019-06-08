# export FLASK_APP=run.py
from modules.compare import compareMain, chunk
import json
from flask import request
from flask import Flask
app = Flask(__name__)

@app.route('/python',methods = ['POST'])
def run():
    j = request.get_json()
    sent1 = chunk(j['teach'])
    sent2 = chunk(j['stud'])
    res = compareMain(sent1,sent2)
    res = json.dumps(res)
    return res


if __name__ == "__main__":
    app.run()


