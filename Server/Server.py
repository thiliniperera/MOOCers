# coding=utf-8
from flask import Flask, render_template, request,redirect,url_for
from Learner import Learner
from Settings import Configurations
import pandas as pd
import os



app = Flask(__name__)

@app.route('/', methods = ['GET', 'POST'])
def index():
    if request.method == 'POST':
        if request.form['username'] == 'admin' and \
                    request.form['password'] == 'admin':
            return redirect(url_for('platform'))

    return render_template('index.html')

@app.route('/analyse')
def platform():
    return render_template('platform.html')

@app.route('/learners')
def learners():
    initialFile = 'static/assets/students.csv'
    df = pd.read_csv(initialFile, nrows=200)

    mylist=[]
    for index, row in df.iterrows():
        an_item = dict(id=row['index'], name=row['name'], grade=row['grade'],location=row['location'],href=index)
        mylist.append(an_item)
    # df=df.apply(lambda x: '<a href="http://example.com/{0}">link</a>'.format(x))
    print mylist
    return render_template('learners.html',mylist= mylist)

@app.route('/csv')
def readDF():
    initialFile = 'static/assets/students.csv'

    df = pd.read_csv(initialFile, nrows=200)
    return df.to_json()

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