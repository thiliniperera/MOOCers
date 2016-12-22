import pandas as pd
import numpy as np

file = 'C://Users//Kushan//Documents//MOOCers//MOOCers//MOOCers Clickstream//Clustering//Sessions//results.csv'

df = pd.read_csv(file, parse_dates=True)
data = pd.DataFrame(df, columns=('NP', 'NB', 'NF', 'MP', 'SR', 'RL', 'AS', 'ES','TP', 'cluster_label','session_no'))

cluster_0 = data[data.cluster_label == 0]
print(len(cluster_0))
cluster_0 = np.mean(cluster_0)

cluster_1 = data[data.cluster_label == 1]
print(len(cluster_1))
cluster_1 = np.mean(cluster_1)

cluster_2 = data[data.cluster_label == 2]
print(len(cluster_2))
cluster_2 = np.mean(cluster_2)

cluster_3 = data[data.cluster_label == 3]
print(len(cluster_3))
cluster_3 = np.mean(cluster_3)

cluster_4 = data[data.cluster_label == 4]
print(len(cluster_4))
cluster_4 = np.mean(cluster_4)

cluster_5 = data[data.cluster_label == 5]
print(len(cluster_5))
cluster_5 = np.mean(cluster_5)

cluster_6 = data[data.cluster_label == 6]
print(len(cluster_6))
cluster_6 = np.mean(cluster_6)

df = pd.DataFrame([cluster_0, cluster_1, cluster_2, cluster_3, cluster_4, cluster_5, cluster_6])

print(df)


length = len(data)


