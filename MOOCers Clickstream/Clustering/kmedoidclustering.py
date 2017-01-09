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
from sklearn import cluster
from scipy.spatial.distance import cdist, pdist
import collections
from sklearn.metrics import silhouette_samples, silhouette_score

Video_code = Configurations.Video_code
file = 'sessions/preprocessed_session'+Video_code[0]+'.csv'

df = pd.read_csv(file, parse_dates=True)
data = pd.DataFrame(df, columns=('user_id','NP', 'NB', 'NF', 'MP', 'SR', 'RL','TP','session_no'))

user_ids = data['user_id']

data = data.drop('user_id', 1)
#data = data.drop('session_no', 1)

#normalizing the columns
data_norm = (data-data.min()) / (data.max()-data.min())

#silhoutte criterion graph
n_clusters = 3
silhouette_avg_list = []
k_means = cluster.KMeans(n_clusters=n_clusters, random_state=10).fit(data_norm)
centroids = k_means.cluster_centers_
cluster_labels = k_means.labels_
silhouette_avg = silhouette_score(data_norm, cluster_labels,sample_size=None, random_state=None,metric='sqeuclidean')
silhouette_avg_list.append(silhouette_avg)
print("For n_clusters =", n_clusters,"The average silhouette_score is :", silhouette_avg)


'''
#elbow method
n = 30
kMeansVar = [KMedoids(n_clusters=k).fit(data_norm) for k in range(1, n)]
centroids = [X.cluster_centers_ for X in kMeansVar]
k_euclid = [cdist(data_norm, cent) for cent in centroids]
dist = [np.min(ke, axis=1) for ke in k_euclid]
wcss = [sum(d**2) for d in dist]
tss = sum(pdist(data_norm)**2)/data_norm.shape[0]
bss = tss - wcss
plt.plot(range(1, n), bss)
plt.show()
'''

#correlation
#data_norm.corr(method='pearson', min_periods=10))
n_clusters = 3
# split into  clusters
k_means = KMedoids(n_clusters=n_clusters, random_state=10).fit(data_norm)

centroids = k_means.cluster_centers_
cluster_labels = k_means.labels_

data_norm['cluster_label'] = cluster_labels
data_norm['user_id'] = user_ids

list = []
for point in centroids:
   list.append(point)
center_points = pd.DataFrame(list,columns=('NP', 'NB', 'NF', 'MP', 'SR', 'RL','TP','session_no'))

label_count = collections.Counter(cluster_labels)
label_list = []
for i in range(n_clusters):
   label_list.append(label_count[i])

center_points['cluster_size'] = label_list

GradesFile = open(Configurations.Grades[0])
df_grades = pd.read_csv(GradesFile, header=None, names=["user_id", "course", "grade", "unknown"])
grades_values = pd.DataFrame(df_grades)
result = pd.merge(left=data_norm, right=grades_values, left_on='user_id', right_on='user_id', how='left')

result = result.drop('unknown', 1)
result = result.drop('course', 1)
result['grade'].fillna(0, inplace=True)
grade_mean = result.groupby(['cluster_label']).mean()
cluster_grades = result.groupby(['cluster_label','grade']).count()
#cluster_dropouts = cluster_grades[cluster_grades.grade == 0]
print(cluster_grades['grade'])
exit()
center_points['mean_grade'] = grade_mean['grade']

fig = plt.figure()
ax = fig.add_subplot(111)
scatter = ax.scatter(data_norm['TP'], data_norm['MP'], c=cluster_labels)
scatter = ax.scatter(centroids[:, 6], centroids[:, 3], c="Red", marker="x", s=100)
fig.savefig('results/'+Video_code[0]+'_'+str(n_clusters)+'.png')
ax.set_xlabel('TP')
ax.set_ylabel('MP')
plt.show()

s = open('results/'+Video_code[0]+'_kmedoid_results'+str(n_clusters)+'.csv', 'w')
center_points.to_csv(s, index=True)

print(center_points)



