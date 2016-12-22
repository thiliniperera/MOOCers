import pandas as pd
from numpy import *
import matplotlib.pyplot as plt


file = 'C://Users//Kushan//Documents//MOOCers//MOOCers//MOOCers Clickstream//Clustering//Sessions//session.csv'

df = pd.read_csv(file, parse_dates=True)
data = pd.DataFrame(df, columns=('NP', 'NB', 'NF', 'MP', 'SR', 'RL', 'AS', 'ES', 'TP', 'session_no'))

nan_positions = isnan(data['MP'])
data[nan_positions] = 0

#data = data[(data.NP != 100) & (data.NB <= 40) & (data.NF <= 40)] # Removing outliers
data = data[data.TP >100]
print(data.describe())
plt.figure()
data.hist()
#plt.show()

s = open('C://Users//Kushan//Documents//MOOCers//MOOCers//MOOCers Clickstream//Clustering//Sessions//preprocessed_session.csv', 'w', newline='')
data.to_csv(s, index=False)
