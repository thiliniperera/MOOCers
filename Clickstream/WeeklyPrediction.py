import pandas as pd
import numpy as np
from threading import _Event
import  datetime
from dateutil.relativedelta import relativedelta
Video = pd.DataFrame()
Event = pd.DataFrame();
Grade = pd.DataFrame();

eventDataLocation = "/home/dinusha/Educational/FYP/HumanitiesandScience_StatLearning_Winter2015/HumanitiesandScience_StatLearning_Winter2015_EventXtract.csv"
finalGradeLocation = "/home/dinusha/Educational/FYP/HumanitiesandScience_StatLearning_Winter2015/HumanitiesandScience_StatLearning_Winter2015_FinalGrade.csv"



def processWekkly(dataset,Grade,fileName):

    student_id = dataset.anon_screen_name.unique()
    grade_array = []
    countfin = 0
    videos = []
    quiz = []
    quiz_count_array = []
    video_count_array = []
    event_count = []
    i = 0
    std = []

    for row_1 in student_id:
        if (i % 500 == 0):
            print i
        std.append(row_1)
        videos = []
        eve_count = 0
        video_count = 0
        quiz_count = 0
        user_records = []
        user_records = dataset[dataset['anon_screen_name'] == row_1]
        video_rec = []
        video_rec = user_records.video_code.unique()
        quiz_rec = user_records[user_records['event_type'] == 'problem_check']
        eve_count = len(user_records)
        quiz_count = len(quiz_rec)
        grade_std = 0
        gra = Grade[Grade['std_id'] == row_1]
        grade_val = gra['grade']
        if (gra.empty):
            grade_std = 0
        else:
            for index,row in gra.iterrows():
                if(row['grade']>0):
                    grade_std=1.0
                else:
                    grade_std=0.0

        video_count = len(video_rec)

        quiz_count_array.append(quiz_count)
        video_count_array.append(video_count)
        event_count.append(eve_count)
        grade_array.append(grade_std)
        i += 1

    np_std = np.array(std)
    np_quiz = np.array(quiz_count_array)
    np_video = np.array(video_count_array)
    np_event = np.array(event_count)
    np_grade = np.array(grade_array)

    pdf = pd.DataFrame({'std_id': np_std, 'quiz': np_quiz, 'video': np_video, 'event': np_event, 'grade': np_grade})
    # print pdf
    # print Grade
    # result = pd.merge(pdf,Grade,on='std_id')
    # print result
    thefile = fileName
    pdf.to_csv(thefile, index=False)


################################################################################################################


f1 = open(eventDataLocation)
f2 = open(finalGradeLocation)
chunksize = 1000000
k = 0;
fields = [0,1,6,8]


for df in pd.read_csv(f1,chunksize=chunksize,low_memory=False,usecols=[0,1,3,6,8]):
    new_column_names = []
    for i in range(0, len(df.columns.values)):
        new_column_names.append(df.columns.values[i].replace("'", ""))
    df.columns = new_column_names
    Event = Event.append(df)
    k+=1
    print k
    if(k>1):
        break
# print Event

fields2 = [0,2]
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

Event['time'] = pd.to_datetime(Event['time'])

unique_year = sorted(Event['time'].dt.year.unique())
print unique_year
month=[]
# for i in unique_year:
#     month[i] = Event[Event['time'].dt.year==i]

Set =  Event[Event['time'].dt.year==2015]
set2 =  Event[Event['time'].dt.year==2014]

set_1 = Set[Set['time'].dt.month==1]
set_2 = Set[Set['time'].dt.month<=2]

set2_1 = set2[set2['time'].dt.month<=10]
set2_2 = set2[set2['time'].dt.month<=11]
set3_3 = set2[set2['time'].dt.month<=12]




print len(set_1)
print len(set_2)
print len(set3_3)

print len(set2_1)
print len(set2_2)

student_id = set3_3.anon_screen_name.unique()

print len(student_id)
result_set_1 = pd.concat([set3_3,set_1])
print "1st month results"
processWekkly(set2_1,Grade,"file0.csv")
print "\n2nd month results"
processWekkly(set2_2,Grade,"file1.csv")
print "\n3rd month results"
processWekkly(set3_3,Grade,"file2.csv")
print "\n4th month results"
processWekkly(result_set_1,Grade,"file3.csv")


print type(Event['time'])


