import csv
import pandas as pd
import numpy as np
from threading import _Event

Video = pd.DataFrame()
Event = pd.DataFrame();
Grade = pd.DataFrame();

#eventDataLocation = "/home/dinusha/Educational/FYP/HumanitiesandScience_StatLearning_Winter2015/HumanitiesandScience_StatLearning_Winter2015_EventXtract.csv"
#finalGradeLocation = "/home/dinusha/Educational/FYP/HumanitiesandScience_StatLearning_Winter2015/HumanitiesandScience_StatLearning_Winter2015_FinalGrade.csv"
eventDataLocation = "/home/dinusha/Educational/FYP/Engineering_CS101_Summer2014/Engineering_CS101_Summer2014_EventXtract.csv"
finalGradeLocation = "/home/dinusha/Educational/FYP/Engineering_CS101_Summer2014/Engineering_CS101_Summer2014_FinalGrade.csv"
f1 = open(eventDataLocation)
f2 = open(finalGradeLocation)
chunksize = 100000
k = 0;
fields = [0,1,6,8]
# df = pd.read_csv(f1, nrows=500,usecols=fields)
# print df
# exit()



for df in pd.read_csv(f1,chunksize=chunksize,low_memory=False,usecols=fields,quoting=csv.QUOTE_NONE):
    new_column_names = []
    for i in range(0, len(df.columns.values)):
        new_column_names.append(df.columns.values[i].replace("'", ""))
    df.columns = new_column_names
    Event = Event.append(df)
    k+=1
    print k

print Event
fields2 =[0,2]
for df in pd.read_csv(f2,chunksize=50000,low_memory=False,names=['std_id','grade'],usecols=fields2,header=None):
    new_column_names = []
    for i in range(0, len(df.columns.values)):
        new_column_names.append(df.columns.values[i])
    df.columns = new_column_names
    Grade = Grade.append(df)
    k+=1
    print k
    if(k>1):
        break

print Grade
student_id = Event.anon_screen_name.unique()
print len(student_id)
#
# print len(student_id)
grade_array = []
countfin = 0
videos = []
quiz = []
quiz_count_array=[]
video_count_array = []
event_count = []
i=0
std = []
for row_1 in student_id:
    if(i%500==0):
        print i
    std.append(row_1)
    videos=[]
    eve_count = 0
    video_count = 0
    quiz_count = 0
    user_records=[]
    user_records = Event[Event['anon_screen_name']==row_1]
    video_rec = []
    video_rec = user_records.video_code.unique()
    quiz_rec = user_records[user_records['event_type']== 'problem_check']
    eve_count = len(user_records)
    quiz_count = len(quiz_rec)
    grade_std =0
    gra = Grade[Grade['std_id']==row_1]
    if(gra.empty):
        grade_std = 0
    else:
        grade_std = gra['grade']

    video_count = len(video_rec)

    quiz_count_array.append(quiz_count)
    video_count_array.append(video_count)
    event_count.append(eve_count)
    grade_array.append(grade_std)
    i+=1


np_std = np.array(std)
np_quiz = np.array(quiz_count_array)
np_video = np.array(video_count_array)
np_event = np.array(event_count)
np_grade = np.array(grade_array)

pdf = pd.DataFrame({'std_id':np_std,'quiz':np_quiz,'video':np_video,'event':np_event,'grade':np_grade})
# print pdf
# print Grade
# result = pd.merge(pdf,Grade,on='std_id')
# print result

thefile = 'final_eng.csv'
pdf.to_csv(thefile,index=False)

