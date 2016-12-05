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

# reading clickstream file
with open(eventDataLocation, 'rt') as f:
    reader = csv.reader(f, delimiter=',')
    for row in islice(reader, 40000, 60000):
        events.append(row)
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
##finding number of activities per user
for row_1 in student_id:
    temp_count = 0
    video_count = 0
    quiz_count = 0
    for row_2 in events:
        if row_2[0] in row_1:
            temp_count += 1
            if row_2[8] not in videos:
                video_count+=1
            if row_2[1] in 'problem_check':
                quiz_count+=1
                quiz.append(row_2[6])
    if temp_count > 100:
        considering_users.append(row_1)
    if quiz_count > 0:
        print quiz_count
    quiz_count_array.append(quiz_count)
    video_count_array.append(video_count)
    event_count.append(temp_count)
#
for row in considering_users:
    for rw in finalGrade:
        if row in rw[0]:
            print row, rw[-2]

# finding number of problems
#for row in events:
  #  print row[1]
