import csv
import pandas as pd
from numpy import *
import numpy as np
import pylab as pl
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from sklearn import cluster
from scipy.spatial.distance import cdist, pdist
from sklearn.metrics import silhouette_samples, silhouette_score

Video_code = ['i4x-Engineering-CS101-video-3f5301fa02fd4b60a541f1497eb3ff64']
file = 'preprocessed_session'+Video_code[0]+'.csv'

df = pd.read_csv(file, parse_dates=True)
data = pd.DataFrame(df, columns=('NP', 'NB', 'NF', 'MP', 'SR', 'RL', 'AS', 'ES', 'session_no'))


#data = data[data.session_no == 1]
nan_positions = isnan(data['MP'])
data[nan_positions] = 0

#preprocessing
data = data[(data.NP <= 100) & (data.NB <= 40) & (data.NF <= 40)] # Removing outliers

#normalizing the columns
'''
max = 505 # hardcoded value of video length found from youtube with video code in data
data_norm = data.drop(labels='session_no', axis=1)
data_norm['SR'] = (data['SR'] / max)*100
data_norm['RL'] = (data['RL'] / max)*100
'''
data_norm = data
data_norm.drop('session_no', axis=1)
data_norm = (data-data.min()) / (data.max()-data.min())


'''
#silhoutte criterion graph
range_n_clusters = [2, 3, 4, 5, 6, 7, 8, 9, 10]
silhouette_avg_list = []
for n_clusters in range_n_clusters:
    k_means = cluster.KMeans(n_clusters=n_clusters, random_state=10).fit(data_norm)
    centroids = k_means.cluster_centers_
    cluster_labels = k_means.labels_
    silhouette_avg = silhouette_score(data_norm, cluster_labels,sample_size=None, random_state=None)
    silhouette_avg_list.append(silhouette_avg)
    print("For n_clusters =", n_clusters,"The average silhouette_score is :", silhouette_avg)


fig = plt.figure()
ax = fig.add_subplot(111)
ax.plot(range_n_clusters, silhouette_avg_list)
plt.show()
'''

'''
#elbow method
n = 15
kMeansVar = [cluster.KMeans(n_clusters=k).fit(data_norm) for k in range(1, n)]
centroids = [X.cluster_centers_ for X in kMeansVar]
k_euclid = [cdist(data_norm, cent) for cent in centroids]
dist = [np.min(ke, axis=1) for ke in k_euclid]
wcss = [sum(d**2) for d in dist]
tss = sum(pdist(data_norm)**2)/data_norm.shape[0]
bss = tss - wcss
plt.plot(range(1, n), bss)
plt.show()
'''


k_means = cluster.KMeans(n_clusters=6, random_state=10).fit(data_norm)
centroids = k_means.cluster_centers_
cluster_labels = k_means.labels_
data_norm['session_no'] = data['session_no']

s = open('results/'+Video_code[0]+'_results.csv', 'w', newline='')
data_norm['cluster_label'] = k_means.labels_
data_norm.to_csv(s, index=False)


fig = plt.figure()
ax = fig.add_subplot(111)
color = ["Red","Yellow","Green"]
scatter = ax.scatter(data_norm['AS'], data_norm['SR'], c=cluster_labels)
scatter = ax.scatter(centroids[:, 0], centroids[:, 1], c="Green", marker="x")
ax.set_xlabel('NF')
ax.set_ylabel('MP')
print(centroids)
plt.show()







