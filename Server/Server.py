# coding=utf-8
from flask import Flask, render_template
from Learner import Learner
import os



app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')



@app.route('/user')
def getUser():
    user = Learner("user","A", 235232)
    return user.toJSON()

@app.route('/analyse/forum')
def analys():
    # os.system('python ForumAnalysis.py')
    return "Analysis initiated"


if __name__ == '__main__':
   app.run()