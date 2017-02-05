# coding=utf-8
from flask import Flask
from Learner import Learner
import os



app = Flask(__name__)

@app.route('/')
def index():
   return 'Analytics platform'



@app.route('/user')
def getUser():
    user = Learner("user","A", 235232)
    return user.toJSON()

@app.route('/analyse/forum')
def getUser():
    os.system('python ForumAnalysis.py')
    return "Analysis initiated"


if __name__ == '__main__':
   app.run()