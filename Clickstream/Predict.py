import pandas as pd
import numpy as np
from sklearn import svm
from sklearn.metrics import accuracy_score
from sklearn.model_selection import cross_val_score

datLocation = "preprocessed.csv"
#datLocation = "file3.csv"
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

training_set = []
data_set = Data[['event','quiz','video','grade']]
#print data_set
training_set = data_set[15000:34000]
test_set = data_set[:15000]
#print test_set
#print training_set['grade']
#test_set = []
#
clf = svm.SVC()

#cross validation
print "first month results"
print cross_val_score(clf,data_set[['event','quiz','video']],data_set['grade'],cv=10)

# clf.fit(training_set[['event','quiz','video']],training_set['grade'])
# output = clf.predict(test_set[['event','quiz','video']])
#
# print "Accuracy",accuracy_score(test_set['grade'],output)