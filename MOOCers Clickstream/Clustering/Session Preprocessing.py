import pandas as pd
from numpy import *
import matplotlib.pyplot as plt
Video_code = ['i4x-Engineering-CS101-video-3f5301fa02fd4b60a541f1497eb3ff64']
file = 'sessions/session_'+Video_code[0]+'.csv'

df = pd.read_csv(file, parse_dates=True)
data = pd.DataFrame(df, columns=('NP', 'NB', 'NF', 'MP', 'SR', 'RL', 'AS', 'ES', 'TP', 'session_no'))

nan_positions = isnan(data['MP'])
data[nan_positions] = 0

#data = data[(data.NP != 100) & (data.NB <= 40) & (data.NF <= 40)] # Removing outliers
data = data[data.TP >100]
print(data.describe())
plt.figure()
data.hist()
plt.show()

s = open('preprocessed_session'+Video_code[0]+'.csv', 'w', newline='')
data.to_csv(s, index=False)
