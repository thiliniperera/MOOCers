import csv
import pandas as pd
import random

finalGradeLocation1 = "/home/dinusha/Educational/FYP/Engineering_CS101_Summer2014/Engineering_CS101_Summer2014_FinalGrade.csv"
finalGradeLocation2 = "/home/dinusha/Educational/FYP/HumanitiesandScience_StatLearning_Winter2015/HumanitiesandScience_StatLearning_Winter2015_FinalGrade.csv"

#f1 = open(finalGradeLocation)

k=0
def processData(location,course_id,filename):
    fields = [0,2]
    chunksize=3000
    Grade = pd.DataFrame()
    k=0
    f1 = open(location)
    for df in pd.read_csv(f1,chunksize=3000,low_memory=False,names=['std_id','grade'],usecols=fields,header=None):
        new_column_names = []
        for i in range(0, len(df.columns.values)):
            new_column_names.append(df.columns.values[i].replace('"',''))
        df.columns = new_column_names
        Grade = Grade.append(df)
        k+=1
        print k
        break

    dropout = []
    courseid = []
    forumscore = []
    for index,row in Grade.iterrows():
        if(row['grade']>0.03):
            dropout.append(0)
        else:
            dropout.append(1)
        courseid.append(course_id)
        forumscore.append("%.2f"%random.uniform(0,0.9))

    Grade['dropout'] = dropout
    Grade['course'] = courseid
    Grade['forum_score'] = forumscore
    print Grade

    file = filename
    Grade.to_csv(file)
    return Grade

eng = pd.DataFrame();
hum = pd.DataFrame();

eng = processData(finalGradeLocation1,0,"eng.csv")
hum = processData(finalGradeLocation2,1,"hum.csv")

res = pd.DataFrame()
res=eng.append(hum)


res.to_csv("res.csv",index=False)