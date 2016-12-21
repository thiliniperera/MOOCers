from numpy import *
import pandas as pd
import matplotlib.pyplot as plt

file = 'C://Users//Kushan//Documents//MOOCers//MOOCers//MOOCers Clickstream//Clustering//Sessions//session.csv'

df = pd.read_csv(file, parse_dates=True)
data = pd.DataFrame(df, columns=('NP', 'NB', 'NF', 'MP', 'SR', 'AS', 'ES'))

nan_positions = isnan(data['MP'])
data[nan_positions] = 0

nan_positions = isnan(data['AS'])
data[nan_positions] = 1

q1 = data.quantile(q=0.25, axis=0, numeric_only=True, interpolation='linear')
q3 = data.quantile(q=0.75, axis=0, numeric_only=True, interpolation='linear')

IQR = q3 - q1
cutoff_val = 1.5 * IQR
print(cutoff_val)
print(len(data))
data = data[(data.NP <= 100) & (data.NB <= 40) & (data.NF <= 40)]
print(len(data))
# notched plot
plt.figure()
plt.boxplot(data['SR'], 0,'gD')
plt.show()
