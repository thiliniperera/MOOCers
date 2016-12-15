import numpy as np
import csv as csv
import pandas as pd
import sklearn as sk
import urllib2
import matplotlib as plt
from itertools import islice

# make sure to change eventDataLocation and finalGradeLocation according your location
eventDataLocation = "/home/dinusha/Educational/FYP/HumanitiesandScience_StatLearning_Winter2015/HumanitiesandScience_StatLearning_Winter2015_EventXtract.csv"
finalGradeLocation = "/home/dinusha/Educational/FYP/HumanitiesandScience_StatLearning_Winter2015/HumanitiesandScience_StatLearning_Winter2015_FinalGrade.csv"

events = []
student_id = []
event_count = []
temp_count = 0
count = 0
finalGrade = []
considering_users = []
videos = []
video_count = 0
video_count_array = []
processed_data = []
quiz = []
quiz_count = 0
quiz_count_array = []
grade_array = []
test_set = []
test_std = []
test_events = []
test_quiz = []
test_videos = []
test_grade = []
# reading clickstream file
with open(eventDataLocation, 'rt') as f:
    reader = csv.reader(f, delimiter=',')
    for row in islice(reader,40000, 45000):
        events.append(row)
    for row in islice(reader,100000,120000):
        test_set.append(row)
#
##reading final grade file
finalGradeData = csv.reader(open(finalGradeLocation), delimiter=",");
# for i in range(2):
#    print reader.next()
for row in finalGradeData:
    finalGrade.append(row)

##finding number of users
for row in events:
    if row[0] not in student_id:
        student_id.append(row[0])
#
for row_1 in student_id:
    for row_2 in finalGrade:
        if row_1 in row_2[0]:
            grade_array.append(row_2[-2])
            break
##finding number of activities per user
for row_1 in student_id:
    temp_count = 0
    video_count = 0
    quiz_count = 0
    for row_2 in events:
        if row_1 in row_2[0]:
            temp_count += 1
            if row_2[8] not in videos and row_2[8] != '':
                video_count+=1
                #              print row_2[1]
            if row_2[1] in 'problem_check':
                quiz_count+=1
                quiz.append(row_2[6])
                #    if temp_count > 100:
                #        considering_users.append(row_1)
                #    if quiz_count > 0:
                #        print quiz_count

    quiz_count_array.append(quiz_count)
    video_count_array.append(video_count)
    event_count.append(temp_count)
#
std_array = np.array(student_id)
quiz_array = np.array(quiz_count_array)
video_array = np.array(video_count_array)
event_array = np.array(event_count)
finalGrade_array = np.array(grade_array)

## Data preprocessing of the test data set
for row in test_set:
    if row[0] not in test_std:
        test_std.append(row[0])
#
for row_1 in test_std:
    for row_2 in finalGrade:
        if row_1 in row_2[0]:
            test_grade.append(row_2[-2])
            break
##finding number of activities per user
for row_1 in test_std:
    temp_count = 0
    video_count = 0
    quiz_count = 0
    for row_2 in test_set:
        if row_1 in row_2[0]:
            temp_count += 1
            if row_2[8] not in test_videos and row_2[8] != '':
                video_count+=1
                #              print row_2[1]
            if row_2[1] in 'problem_check':
                quiz_count+=1
                quiz.append(row_2[6])

    test_quiz.append(quiz_count)
    test_videos.append(video_count)
    test_events.append(temp_count)

t_quiz = np.array(test_quiz)
t_video = np.array(test_videos)
t_events = np.array(test_events)
t_grade = np.array(test_grade)
final_test_array = np.stack((t_quiz,t_video,t_events,t_grade))

finalArray = np.stack((quiz_array, video_array, event_array,finalGrade_array))
#for row in finalArray:
#    print row


clf = sk.svm.LinearSVC()
clf.fit(finalArray[:3],finalArray[3])
clf.predict(final_test_array[:3],final_test_array[3])
# finding number of problems
#for row in events:
  #  print row[1]
