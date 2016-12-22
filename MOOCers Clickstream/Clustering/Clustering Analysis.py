import pandas as pd
import numpy as np

Video_code = ['i4x-Engineering-CS101-video-3f5301fa02fd4b60a541f1497eb3ff64']
file = 'results/'+Video_code[0]+'_results.csv'

df = pd.read_csv(file, parse_dates=True)
data = pd.DataFrame(df, columns=('NP', 'NB', 'NF', 'MP', 'SR', 'RL', 'AS', 'ES', 'cluster_label','session_no'))

cluster_0 = data[data.cluster_label == 0]
cluster_len_0 = len(cluster_0)
cluster_0 = np.mean(cluster_0)

cluster_1 = data[data.cluster_label == 1]
cluster_len_1 = len(cluster_1)
cluster_1 = np.mean(cluster_1)

cluster_2 = data[data.cluster_label == 2]
cluster_len_2 = len(cluster_2)
cluster_2 = np.mean(cluster_2)

cluster_3 = data[data.cluster_label == 3]
cluster_len_3 = len(cluster_3)
cluster_3 = np.mean(cluster_3)

cluster_4 = data[data.cluster_label == 4]
cluster_len_4 = len(cluster_4)
cluster_4 = np.mean(cluster_4)

cluster_5 = data[data.cluster_label == 5]
cluster_len_5 = len(cluster_5)
cluster_5 = np.mean(cluster_5)



df = pd.DataFrame([cluster_0, cluster_1, cluster_2, cluster_3, cluster_4, cluster_5])
df['no_of_sessions'] = [cluster_len_0,cluster_len_1,cluster_len_2,cluster_len_3,cluster_len_4,cluster_len_5]

print(df)


length = len(data)


