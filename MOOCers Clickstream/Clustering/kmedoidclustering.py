from numpy import *
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import DBSCAN
from kmedoid import kMedoids
from sklearn import metrics
import numpy as np
from sklearn.metrics.pairwise import pairwise_distances
from sklearn.datasets.samples_generator import make_blobs
from sklearn.preprocessing import StandardScaler
from settings import Configurations

Video_code = Configurations.Video_code
file = 'sessions/preprocessed_session'+Video_code[0]+'.csv'

df = pd.read_csv(file, parse_dates=True)
data = pd.DataFrame(df, columns=('user_id','NP', 'NB', 'NF', 'MP', 'SR', 'RL', 'AS', 'ES','TP','session_no'))

user_ids = data['user_id']
data = data.drop('user_id', 1)

nan_positions = isnan(data['MP'])
data[nan_positions] = 0

#normalizing the columns
data_norm= (data-data.min()) / (data.max()-data.min())

#correlation
print(data_norm.corr(method='pearson', min_periods=10))

# distance matrix
D = pairwise_distances(data_norm, metric='euclidean')

# split into  clusters
M, C = kMedoids(D, 5)
centroids = pd.DataFrame()

for point in M:
    centroids = centroids.append(data_norm.iloc[point])

print(centroids)

clusters = [None] * len(data_norm)
for label in C:
    for point_idx in C[label]:
        clusters[point_idx] = label


cluster_labels = [float(item) for item in clusters]

fig = plt.figure()
ax = fig.add_subplot(111)
scatter = ax.scatter(data_norm['TP'], data_norm['MP'], c=cluster_labels)
scatter = ax.scatter(centroids['TP'], centroids['MP'], c="Red", marker="x",s=100)
ax.set_xlabel('TP')
ax.set_ylabel('MP')
plt.show()

data_norm['cluster_label'] = clusters
data_norm['user_id'] = user_ids

s = open('results/'+Video_code[0]+'_kmedoid_results.csv', 'w')
data_norm.to_csv(s, index=False)


