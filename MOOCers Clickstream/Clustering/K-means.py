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

file = 'C://Users//Kushan//Documents//MOOCers//MOOCers//MOOCers Clickstream//Clustering//Sessions//preprocessed_session.csv'

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



k_means = cluster.KMeans(n_clusters=6, random_state=10).fit(data_norm)
centroids = k_means.cluster_centers_
cluster_labels = k_means.labels_
data_norm['session_no'] = data['session_no']

s = open('C://Users//Kushan//Documents//MOOCers//MOOCers//MOOCers Clickstream//Clustering//Sessions//results.csv', 'w', newline='')
data_norm['cluster_label'] = k_means.labels_
data_norm.to_csv(s, index=False)

i = 0
j = 0
k = 0
for row in cluster_labels:
    if row == 0:
        i = i +1
    if row == 1:
        j = j +1
    if row == 2:
        k = k +1

print("Cluster 0 :", i)
print("Cluster 1 :", j)
print("Cluster 2 :", k)


fig = plt.figure()
ax = fig.add_subplot(111)
color = ["Red","Yellow","Green"]
scatter = ax.scatter(data_norm['AS'], data_norm['SR'], c=cluster_labels)
scatter = ax.scatter(centroids[:, 0], centroids[:, 1], c="Green", marker="x")
ax.set_xlabel('NF')
ax.set_ylabel('MP')
print(centroids)
plt.show()







