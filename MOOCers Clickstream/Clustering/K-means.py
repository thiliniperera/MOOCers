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

file = 'C://Users//Kushan//Documents//MOOCers//MOOCers//MOOCers Clickstream//Clustering//Sessions//session.csv'

df = pd.read_csv(file, parse_dates=True)
data = pd.DataFrame(df, columns=('NP', 'NB', 'NF', 'MP', 'SR', 'AS', 'ES'))

original_length = len(data)

#data = data[(data['NP'] > 0) | (data['NB'] > 0) | (data['NF'] > 0)]
#print("Removed percentage: ", ((original_length-len(data))/original_length)*100)

nan_positions = isnan(data['MP'])
data[nan_positions] = 0

nan_positions = isnan(data['AS'])
data[nan_positions] = 1

#normalizing the columns
data_norm = (data - data.min()) / (data.max() - data.min())

'''
#silhoutte criterion graph
range_n_clusters = [2, 3, 4, 5, 6, 7]
silhouette_avg_list = []

for n_clusters in range_n_clusters:
    k_means = cluster.KMeans(n_clusters=n_clusters, random_state=10).fit(data_norm)
    centroids = k_means.cluster_centers_
    cluster_labels = k_means.labels_
    silhouette_avg = silhouette_score(data_norm, cluster_labels,metric='manhattan')
    silhouette_avg_list.append(silhouette_avg)
    print("For n_clusters =", n_clusters,"The average silhouette_score is :", silhouette_avg)


fig = plt.figure()
ax = fig.add_subplot(111)
ax.plot(range_n_clusters, silhouette_avg_list)
plt.show()
'''

'''
#elbow method
n = 10
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


k_means = cluster.KMeans(n_clusters=3, random_state=10).fit(data_norm)
centroids = k_means.cluster_centers_
cluster_labels = k_means.labels_

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
scatter = ax.scatter(data_norm['ES'], data_norm['AS'], c=cluster_labels)
scatter = ax.scatter(centroids[:, 0], centroids[:, 1], c="Red", marker="x")
ax.set_xlabel('NF')
ax.set_ylabel('MP')
print(centroids)
plt.show()


'''
threedee = plt.figure().gca(projection='3d')
threedee.scatter(data_norm['NF'], data['NP'],data_norm['NB'], c=k_means.labels_)
threedee.scatter(k_means.cluster_centers_[:, 0], k_means.cluster_centers_[:, 1],c="Red", marker='x')
threedee.set_xlabel('NF')
threedee.set_ylabel('NP')
threedee.set_zlabel('NB')
plt.show()

'''






