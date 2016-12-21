import pandas as pd
import numpy as np

file = 'C://Users//Kushan//Documents//MOOCers//MOOCers//MOOCers Clickstream//Clustering//Sessions//results.csv'

df = pd.read_csv(file, parse_dates=True)
data = pd.DataFrame(df, columns=('NP', 'NB', 'NF', 'MP', 'SR', 'RL', 'AS', 'ES', 'cluster_label','session_no'))

cluster_0 = data[data.cluster_label == 0]
cluster_0 = np.mean(cluster_0)

cluster_1 = data[data.cluster_label == 1]
cluster_1 = np.mean(cluster_1)

cluster_2 = data[data.cluster_label == 2]
cluster_2 = np.mean(cluster_2)

df = pd.DataFrame([cluster_0, cluster_1, cluster_2])

print(df)

test_val = len(data[(data.cluster_label == 0) & (data.session_no == 1)])
print(test_val)

length = len(data)

print(test_val/length)



