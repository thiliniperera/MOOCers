import pandas as pd
from numpy import *
import matplotlib.pyplot as plt
from settings import Configurations

#preprocess NB,NP,NF, mP
def preprocess(data,S,bin):
    bin_size = bin
    df = pd.DataFrame()
    res = pd.cut(data[S],bin_size)
    count = pd.value_counts(res)
    df['count'] = count.reindex(res.cat.categories)
    count = count.reindex(res.cat.categories)

    i=0;
    zero_count =0;
    for index,x in df.iterrows():
        if x['count'] == 0:
            zero_count+=1
            if(zero_count > (float (bin_size)/10)):
                start_value = float(index[index.index("(")+1:index.index(",")])
                end_value = float(index[index.index(",")+1:index.index("]")])
                data = data[data[S]<end_value]
                return data
                break
        else:
            zero_count =0
        i+=1
    return data

#preprocess speed rate
def preprocessAS(data,Att):
    max = data[Att].max()
    min = data[Att].min()

    if max <= 2.0 and min >= 0.5:
        print "No outliers"
        return data
    else:
       data = data[(data[Att] <=2.0) & (data[Att] >= 0.5)]
       return data

def preprocessES(data,Att):
    max = data[Att].max()
    min = data[Att].min()

    if max <= 1.5 and min >= -1.5:
        print "No outliers"
        return data
    else:
       data = data[(data[Att] <=1.5) & (data[Att] >= -1.5)]
       return data
    
fileLocation = 'session.csv'

file = 'C://Users//Kushan//Documents//MOOCers//MOOCers//MOOCers Clickstream//Clustering//Sessions//session.csv'
df = pd.read_csv(fileLocation, parse_dates=True)

data = pd.DataFrame(df, columns=('NP', 'NB', 'NF', 'MP', 'SR', 'RL', 'AS', 'ES', 'TP', 'session_no'))
Video_code = Configurations.Video_code

file = 'sessions/session_'+Video_code[0]+'.csv'
#
# df = pd.read_csv(file, parse_dates=True)
# data = pd.DataFrame(df, columns=('NP', 'NB', 'NF', 'MP', 'SR', 'AS','RL','TP', 'ES', 'session_no'))

nan_positions = isnan(data['MP'])
data[nan_positions] = 0
data = data[data.TP > 100]
print(data.describe())
plt.figure()
data.hist()
print "NP"
data = preprocess(data,'NP',30)
print "NF"
data=preprocess(data,'NF',30)
print "NB"
data=preprocess(data,'NB',30)
print "MP"
data=preprocess(data,'MP',30)
print "AS"
data = preprocessAS(data,'AS')
print "SR"
data = preprocess(data,'SR',100)
print "RL"
data = preprocess(data,'RL',50)
print "ES"
data = preprocessES(data,'ES')
print data.describe()

#plt.show()
wrtLocation = open('preprocessed_session.csv','w')
#s = open('C://Users//Kushan//Documents//MOOCers//MOOCers//MOOCers Clickstream//Clustering//Sessions//preprocessed_session.csv', 'w', newline='')

data.to_csv(wrtLocation, index=False)
data['TP'].hist()
plt.show()

s = open('preprocessed_session'+Video_code[0]+'.csv', 'w')
data.to_csv(s, index=False)

