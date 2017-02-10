# coding=utf-8
from flask import Flask, render_template, request, redirect, url_for
from Learner import Learner
from Settings import Configurations
import pandas as pd
import os
import flask_login

app = Flask(__name__)
app.secret_key = 'Mo0c Analytics'
login_manager = flask_login.LoginManager()

login_manager.init_app(app)

# Our mock database.
users = {'kasun.bdn@gmail.com': {'pw': 'pass'}}


class User(flask_login.UserMixin):
    pass

    @login_manager.user_loader
    def user_loader(email):
        if email not in users:
            return

        user = User()
        user.id = email
        return user

    @login_manager.request_loader
    def request_loader(request):
        email = request.form.get('email')
        if email not in users:
            return

        user = User()
        user.id = email

        # DO NOT ever store passwords in plaintext and always compare password
        # hashes using constant-time comparison!
        user.is_authenticated = request.form['pw'] == users[email]['pw']

        return user


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return '''
               <form action='login' method='POST'>
                <input type='text' name='email' id='email' placeholder='email'></input>
                <input type='password' name='pw' id='pw' placeholder='password'></input>
                <input type='submit' name='submit'></input>
               </form>
               '''

    email = request.form['email']
    if request.form['pw'] == users[email]['pw']:
        user = User()
        user.id = email
        flask_login.login_user(user)
        return redirect(url_for('protected'))

    return 'Bad login'


@app.route('/protected')
@flask_login.login_required
def protected():
    return 'Logged in as: ' + flask_login.current_user.id


@app.route('/logout')
def logout():
    flask_login.logout_user()
    return 'Logged out'


@login_manager.unauthorized_handler
def unauthorized_handler():
    return 'Unauthorized user'


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if request.form['username'] == 'admin' and \
                        request.form['password'] == 'admin':
            return redirect(url_for('platform'))

    return render_template('index.html')


@app.route('/courses')
def courses():
    return render_template('courses.html')


@app.route('/platform')
def platform():
    return render_template('platform.html')


@app.route('/learners')
def learners():
    initialFile = 'static/assets/students.csv'
    df = pd.read_csv(initialFile, nrows=200)

    mylist = []
    for index, row in df.iterrows():
        an_item = dict(id=row['index'], name=row['name'], grade=row['grade'], location=row['location'], href=index)
        mylist.append(an_item)
    # df=df.apply(lambda x: '<a href="http://example.com/{0}">link</a>'.format(x))
    # print mylist
    return render_template('learners.html', mylist=mylist)


@app.route('/learners/<userid>')
def getUserinfo(userid=None):
    initialFile = 'static/assets/students.csv'
    df = pd.read_csv(initialFile, nrows=200)
    # print df.irow(userid)
    return render_template('user.html', name=df.irow(userid))


@app.route('/csv')
def readDF():
    initialFile = 'static/assets/students.csv'

    df = pd.read_csv(initialFile, nrows=200)
    return df.to_html()


@app.route('/user')
def getUser():
    user = Learner("user", "A", 235232)
    return user.toJSON()

@app.route('/forum')
def forum():
    return render_template('forum.html')


if __name__ == '__main__':
    app.run()
