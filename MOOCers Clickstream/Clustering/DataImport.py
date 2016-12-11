import numpy as np
import csv
import itertools
Video_code = ['i4x-Engineering-CS101-video-z68']
f = open('C://Users//Kushan//Documents//MOOCers//MOOCers//MOOCers Clickstream//Clustering//Videos//'+Video_code[0]+'.csv')
csv_f = csv.reader(f)

s = open('C://Users//Kushan//Documents//MOOCers//MOOCers//MOOCers Clickstream//Clustering//Sessions//session.csv', 'w', newline='')
csv_session = csv.writer(s)
session = ['user_id','NP','NB','NF']
csv_session.writerow(session);

#Getting N rows as the data set
data = []
#for row in itertools.islice(csv_f,1,10000):
for row in csv_f:
    data.append(row)

#reading the unique student ids into a list
student_ids = []
for row in data:
    if row[13] not in student_ids:
        student_ids.append(row[13])

#for each student create activity sequence
for student in student_ids:
    print(student);
    activity_list = []
    for row in data:
        if row[13] == student:
            activity_list.append(row)
    activity_list.sort(key=lambda tup: tup[10])

    #find the no of pauses NP
    NP = sum(x[0] == 'pause_video' for x in activity_list)
    print("NP: ", NP);

    '''
    #Median duration of pauses
    pause_duration = []
    for row in activity_list:
        if row[0] == 'pause_video':
    '''

    #no of forward seeks
    NB = sum(x[0]=='seek_video' and x[6]<x[7] for x in activity_list)
    NF = sum(x[0] == 'seek_video' and x[6] > x[7] for x in activity_list)
    print("NB: ",NB);
    print("NF: ",NF);

    session = []
    session.append(student)
    session.append(NP)
    session.append(NB)
    session.append(NF)
    csv_session.writerow(session);

    w = 'C://Users//Kushan//Documents//MOOCers//MOOCers//MOOCers Clickstream//Clustering//Videos//'+(student)+'.csv'

    with open(w, 'w', newline='') as mycsvfile:
        thedatawriter = csv.writer(mycsvfile)
        for row in activity_list:
            thedatawriter.writerow(row)











