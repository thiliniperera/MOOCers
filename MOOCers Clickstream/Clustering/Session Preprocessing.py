import pandas as pd
from numpy import *
import matplotlib.pyplot as plt
from settings import Configurations

#preprocess NB,NP,NF, mP
def preprocess(data,S):

    df = pd.DataFrame()
    df2 = pd.DataFrame()
    res = pd.cut(data[S],30)
    data['result'] = pd.cut(data[S],30)
    count = pd.value_counts(res)
    df['count'] = count.reindex(res.cat.categories)
    count = count.reindex(res.cat.categories)
    #print df['count']
    i=0;
    for index,x in df.iterrows():
        if x['count'] == 0:
            print "0 index", i
        else:
            print x['count']
        i+=1
    return

#preprocess speed rate
def preprocessAS(data):
    max = data.max()
    min = data.min()
    df = pd.DataFrame({'Data':data})

    if max <= 1.75 and min >= 0.75:
        print "No outliers"
        return
    else:
       data = data[(data <=1.75) & (data >= 0.75)]
       print data.describe()
    #print data

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
#data = data[(data.NP != 100) & (data.NB <= 40) & (data.NF <= 40)] # Removing outliers
data = data[data.TP > 100]
data = data[data.TP < 2000]
print(data.describe())
plt.figure()
data.hist()
print "NP"
preprocess(data,'NP')
print "NB"
preprocess(data,'NB')
print "TP"
preprocess(data,'TP')
print "AS"
preprocessAS(data['AS'])
#preprocess(data,'ES')
plt.show()
wrtLocation = open('preprocessed_session.csv','w')
#s = open('C://Users//Kushan//Documents//MOOCers//MOOCers//MOOCers Clickstream//Clustering//Sessions//preprocessed_session.csv', 'w', newline='')

data.to_csv(wrtLocation, index=False)
data['TP'].hist()
plt.show()

s = open('preprocessed_session'+Video_code[0]+'.csv', 'w')
data.to_csv(s, index=False)

