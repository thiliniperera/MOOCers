# coding=utf-8
from flask import Flask, render_template, request, redirect, url_for, send_from_directory, json
from dateutil.parser import parse
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

student_csv = 'static/assets/students.csv'
student_df = pd.read_csv(student_csv)

course_csv = 'static/assets/course.csv'
course_df = pd.read_csv(course_csv)

student_course_csv = 'static/assets/student_course.csv'
student_course_df = pd.read_csv(student_course_csv)

student_demo_csv = 'static/assets/students_demo.csv'
student_demo_df = pd.read_csv(student_demo_csv)


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
        else:
            return render_template('login.html', message='username or password mismatch!')
    except:
        return render_template('login.html', message='username or password mismatch!')


@app.route('/search', methods=['POST'])
@flask_login.login_required
def search():
    query = request.form['query']
    search_result = student_demo_df[student_demo_df['name'].str.contains(pat=query, case=False)]

    # or student_df['index'].str.contains(query)
    mylist = []
    i = 0
    for index, row in search_result.iterrows():
        i = i + 1
        gender = 'Male'
        if (row['gender'] == 'f'):
            gender = 'Female'
        an_item = dict(id=i, name=row['name'], gender=gender, location=row['country_name'])
        mylist.append(an_item)

    return render_template('search_result.html', mylist=mylist)


@app.route('/course/dropout/<course_id>')
@flask_login.login_required
def dropout(course_id):
    data = student_course_df[student_course_df['course'] == int(course_id)]
    if (len(data)):
        mylist = []
        i = 0
        for index, row in data[data['dropout_status'] == 1].iterrows():
            i = i + 1
            dropout = row['dropout_status']
            if (int(dropout) == 1):
                dropout = 'Dropout'
            else:
                dropout = 'Active'
            an_item = dict(id=i, name=row['name'], grade=row['performance'], dropout=dropout)
            mylist.append(an_item)
        return render_template('course_dropouts.html', mylist=mylist)
    else:
        return "No students are going to drop out the course"


@app.route('/user_profile/<username>')
@flask_login.login_required
def getUserinfo(username=None):
    # print df.irow(userid)
    # row = student_df.irow(username)
    data = student_demo_df[student_demo_df['name'] == username]

    if (len(data) > 0):
        row = data.irow(0)
        gender = 'Male'
        if (row['gender'] == 'f'):
            gender = 'Female'

        course_data_list = []
        predicted_data = student_course_df[student_course_df['name'] == username]
        if (len(predicted_data) > 0):
            for index, course_row in predicted_data.iterrows():
                dropout = course_row['dropout_status']
                if (int(dropout) == 1):
                    dropout = 'Dropout'
                else:
                    dropout = 'Active'

                an_item = dict(performance=course_row['performance'], dropout=dropout,
                               forum_score=course_row['forum_score'],
                               course_name=course_df.irow(int(course_row['course']))['name'])
                course_data_list.append(an_item)

        return render_template('learner_profile.html', name=row['name'], gender=gender,
                               location=row['country_name'],
                               year_of_birth=row['year_of_birth'],
                               level_of_education=row['level_of_education'], course_list=course_data_list)
    else:
        json.dumps({'success': False}), 404, {'ContentType': 'application/json'}


@app.route('/logout')
def logout():
    flask_login.logout_user()
    return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}


@login_manager.unauthorized_handler
def unauthorized_handler():
    return redirect(url_for('login'))


@app.route('/courses/<course_id>')
@flask_login.login_required
def courses(course_id=None):
    if (int(course_id) >= len(course_df)):
        course_id = 0
    row = course_df.irow(course_id)
    course_name = str(row['name']) + " , " + row['term'] + " " + str(parse(str(row['starting_date'])).year)
    return render_template('courses.html', no_of_students=row['no_of_students'], no_of_videos=row['no_of_videos'],
                           no_of_assignments=row['no_of_assignments'], name=course_name)


@app.route('/')
@flask_login.login_required
def platform():
    mylist = []
    completed_percentage = [55, 48, 50]  # need to calculated from start date and end date in a real implementation
    i = 0
    for index, row in course_df.iterrows():
        course_name = str(row['name']) + " , " + row['term'] + " " + str(parse(str(row['starting_date'])).year)
        an_item = dict(id=index, starting_date=row['starting_date'],
                       ending_date=row['ending_date'],
                       no_of_students=row['no_of_students'],
                       no_of_videos=row['no_of_videos'],
                       no_of_assignments=row['no_of_assignments'],
                       name=course_name,
                       students_at_risk=row['at_risk'],
                       completed_percentage=completed_percentage[i]
                       )
        mylist.append(an_item)
        i = i + 1
    return render_template('platform.html', course_list=mylist)


@app.route('/learners')
@flask_login.login_required
def learners():
    no_of_records = len(student_course_df)
    no_of_isolated_students = len(student_course_df[student_course_df['forum_score'] < 0.2])
    no_of_at_rik_students = len(student_course_df[student_course_df['dropout_status'] == 1])
    return render_template('learners.html', total=no_of_records, current_students=no_of_records,
                           no_of_isolated_students=no_of_isolated_students, no_of_at_rik_students=no_of_at_rik_students)


@app.route('/csv/<course_id>')
@flask_login.login_required
def readDF(course_id=0):
    return student_df.to_html()


@app.route('/forum/<courseid>')
@flask_login.login_required
def forum(courseid):
    return render_template('forum.html')


@app.route('/json/<path:path>')
@flask_login.login_required
def send_json(path):
    return send_from_directory(app.static_folder, path)


@app.route('/community/<courseid>')
@flask_login.login_required
def community(courseid=None):
    return render_template('community.html')


if __name__ == '__main__':
    app.run()
