# coding=utf-8
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from Settings import Configurations
import pandas as pd
import os
import flask_login

app = Flask(__name__)
app.secret_key = 'Mo0c Analytics'
login_manager = flask_login.LoginManager()

login_manager.init_app(app)

# Our mock database.
users = {'kasun': {'pw': 'pass'},
         'admin': {'pw': 'admin'},
         'demo': {'pw': 'demo'}}


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
        return render_template('login.html')

    try:
        uName = request.form['username']
        if request.form['password'] == users[uName]['pw']:
            user = User()
            user.id = uName
            flask_login.login_user(user)
            return redirect(url_for('platform'))
    except:
        return render_template('login.html', message='username or password mismatch!')


@app.route('/protected')
@flask_login.login_required
def protected():
    return 'Logged in as: ' + flask_login.current_user.id


@app.route('/logout')
def logout():
    flask_login.logout_user()
    return redirect(url_for('login'))


@login_manager.unauthorized_handler
def unauthorized_handler():
    return redirect(url_for('login'))


@app.route('/courses')
@flask_login.login_required
def courses():
    return render_template('courses.html')


@app.route('/')
@flask_login.login_required
def platform():
    return render_template('platform.html')


@app.route('/learners')
@flask_login.login_required
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
@flask_login.login_required
def getUserinfo(userid=None):
    initial_file = 'static/assets/students.csv'
    df = pd.read_csv(initial_file, nrows=200)
    # print df.irow(userid)
    return render_template('user.html', name=df.irow(userid))


@app.route('/csv')
@flask_login.login_required
def readDF():
    initialFile = 'static/assets/students.csv'

    df = pd.read_csv(initialFile, nrows=200)
    return df.to_html()


@app.route('/forum')
@flask_login.login_required
def forum():
    return render_template('forum.html')

@app.route('/course/dropout')
@flask_login.login_required
def dropout():
    initialFile = 'static/assets/students.csv'
    df = pd.read_csv(initialFile, nrows=200)

    mylist = []
    for index, row in df.iterrows():
        an_item = dict(id=row['index'], name=row['name'], grade=row['grade'], location=row['location'], href=index)
        mylist.append(an_item)
    return render_template('course_dropouts.html',mylist=mylist)

@app.route('/json/<path:path>')
@flask_login.login_required
def send_json(path):
    print path
    return send_from_directory(app.static_folder, path)


if __name__ == '__main__':
    app.run()
