# export FLASK_APP=run.py
from modules.compare import compareMain, chunk
import json
from flask import request
from flask import Flask
app = Flask(__name__)

@app.route('/python',methods = ['POST'])
def lol():
    j = request.get_json()
    print(j['teach'])
    print(j['stud'])
    sent1 = chunk(j['teach'])
    sent2 = chunk(j['stud'])
    compareMain(sent1,sent2)
    return 'done'

app.run()