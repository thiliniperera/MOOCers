from numpy import *
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import DBSCAN
from kmedoid import KMedoids
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

#normalizing the columns
data_norm= (data-data.min()) / (data.max()-data.min())

#correlation
#data_norm.corr(method='pearson', min_periods=10))

# distance matrix
D = pairwise_distances(data_norm, metric='euclidean')

# split into  clusters
k_means = KMedoids(n_clusters=5, random_state=10).fit(data_norm)

centroids = k_means.cluster_centers_
cluster_labels = k_means.labels_

list = []
for point in centroids:
   list.append(point)

center_points = pd.DataFrame(list,columns=('NP', 'NB', 'NF', 'MP', 'SR', 'RL', 'AS', 'ES','TP','session_no'))
print(center_points)

fig = plt.figure()
ax = fig.add_subplot(111)
scatter = ax.scatter(data_norm['MP'], data_norm['TP'], c=cluster_labels)
scatter = ax.scatter(centroids[:, 3], centroids[:, 8], c="Red", marker="x", s=100)
ax.set_xlabel('MP')
ax.set_ylabel('TP')
plt.show()

data_norm['cluster_label'] = cluster_labels
data_norm['user_id'] = user_ids

s = open('results/'+Video_code[0]+'_kmedoid_results.csv', 'w')
data_norm.to_csv(s, index=False)


