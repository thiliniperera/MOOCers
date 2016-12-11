import csv
import pandas as pd
import numpy as np
import pylab as pl
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from sklearn import cluster

file = 'C://Users//Kushan//Documents//MOOCers//MOOCers//MOOCers Clickstream//Clustering//Sessions//session.csv'

df = pd.read_csv(file, parse_dates=True)
data = pd.DataFrame(df, columns=('NP', 'NB', 'NF'))

original_length = len(data)

data = data[(data['NP'] > 0) | (data['NB'] > 0) | (data['NF'] > 0)]

print("Removed percentage: ", ((original_length-len(data))/original_length)*100)

k_means = cluster.KMeans(n_clusters=5, random_state=0).fit(data)

centroids = k_means.cluster_centers_
cluster_labels = k_means.labels_

fig = plt.figure()
ax = fig.add_subplot(111)
scatter = ax.scatter(data['NP'], data['NB'], c=cluster_labels)
scatter = ax.scatter(centroids[:, 0], centroids[:, 1], c="Red", marker="x")

ax.set_xlabel('x')
ax.set_ylabel('y')

plt.show()

'''
threedee = plt.figure().gca(projection='2d')
threedee.scatter(data['NF'], data['NP'], c=k_means.labels_)
threedee.scatter(k_means.cluster_centers_[:, 0], k_means.cluster_centers_[:, 1],c="Red", marker='x')
threedee.set_xlabel('NF')
threedee.set_ylabel('NP')
threedee.set_zlabel('NB')
plt.show()
'''







