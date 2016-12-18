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
videos = []
video_count = 0
video_count_array = []
processed_data = []
quiz = []
quiz_count = 0
quiz_count_array = []
grade_array = []
training_set = []
test_set= []
# reading clickstream file
with open(eventDataLocation, 'rt') as f:
   reader = csv.reader(f, delimiter=',')
   for row in islice(reader,30000, 30100):
       events.append(row)

##reading final grade file
finalGradeData = csv.reader(open(finalGradeLocation), delimiter=',');
# for i in range(2):
#    print reader.next()
for row in finalGradeData:
    finalGrade.append(row)
print len(finalGrade)
##finding number of users
for row in events:
    if row[0] not in student_id:
        student_id.append(row[0])
#
# for row_1 in student_id:
#     for row_2 in finalGrade:
#         if row_1 in row_2[0]:
#             grade_array.append(row_2[-2])
#             break
##finding number of activities per user
countfin =0
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
    for row_3 in finalGrade:
        if row_1 in row_3[0]:
            countfin+=1
            grade_array.append(row_3[-2])
            break
    quiz_count_array.append(quiz_count)
    video_count_array.append(video_count)
    event_count.append(temp_count)
#
std_array = np.array(student_id)
quiz_array = np.array(quiz_count_array)
video_array = np.array(video_count_array)
event_array = np.array(event_count)
finalGrade_array = np.array(grade_array)

print (len(std_array))
print (len(quiz_array))
print (len(video_array))
print (len(event_array))
print len(finalGrade_array)
print countfin
finalArray = np.stack((quiz_array, video_array, event_array))

#print(len(finalArray))
# training_set = finalArray
#
# clf = sk.svm.LinearSVC()
# clf.fit(finalArray[:3],finalArray[3])
#clf.predict(final_test_array[:3],final_test_array[3])
# finding number of problems
#for row in events:
  #  print row[1]
