import pandas as pd
import numpy as np

datLocation = "finalArray.csv"
file_1 = open(datLocation)
chunksize=35000
k=0

Data = pd.DataFrame()

for df in pd.read_csv(file_1,chunksize=chunksize,low_memory=False):
    new_column_names = []
    for i in range(0, len(df.columns.values)):
        new_column_names.append(df.columns.values[i].replace("'", ""))
    df.columns = new_column_names
    Data = Data.append(df)
    k+=1
    print k
    if(k>5):
        break

modifiedgrade=[]
for index,row in Data.iterrows():
    if(row['grade']>0):
        row['grade']=1.0
    else:
        row['grade']=0.0
    modifiedgrade.append(row['grade'])

modi_grade = np.array(modifiedgrade)
pdf = pd.DataFrame({'grade':modi_grade})
# print pdf
# print Data
Data['grade'] = pdf['grade']
# print "AFter"
# print Data

Data.to_csv('preprocessed.csv',index=False)