import pandas as pd
from numpy import *
import matplotlib.pyplot as plt
from settings import Configurations

Video_code = Configurations.Video_code

file = 'sessions/session_'+Video_code[0]+'.csv'

df = pd.read_csv(file, parse_dates=True)
data = pd.DataFrame(df, columns=('NP', 'NB', 'NF', 'MP', 'SR', 'AS','RL','TP', 'ES', 'session_no'))

nan_positions = isnan(data['MP'])
data[nan_positions] = 0

#data = data[(data.NP != 100) & (data.NB <= 40) & (data.NF <= 40)] # Removing outliers
data = data[data.TP > 100]
data = data[data.TP < 2000]
print(data.describe())
plt.figure()
data['TP'].hist()
plt.show()

print(len(data))

s = open('preprocessed_session'+Video_code[0]+'.csv', 'w')
data.to_csv(s, index=False)
