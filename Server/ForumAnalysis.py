from __future__ import division
import pandas as pd
import numpy as np
import igraph
import matplotlib.pyplot as plt

from Settings import Configurations

initialFile = open(Configurations.InitialForumDataFile[0])

df = pd.read_csv(initialFile, nrows=500)
uniqueUsers = df['anon_screen_name'].unique()
users = df['anon_screen_name'].values
uniqueCommentThreadIDs =  df[df['type'] == 'CommentThread']['forum_post_id'].unique()

commentThreadIDs = df['forum_post_id'].where(df['type'] == 'CommentThread', df['comment_thread_id']).values

# df['forum_id'] = commentThreadIDs
xDim= len(uniqueUsers)
yDim= len(uniqueCommentThreadIDs)
totalLoops = xDim*yDim
print xDim
print yDim
print len(commentThreadIDs)

initialArray = [[0 for x in range(len(uniqueCommentThreadIDs))] for y in range(len(uniqueUsers))]

for i in range(len(uniqueUsers)):
    for j in range(len(uniqueCommentThreadIDs)):
        involvement = 0
        for k in range(len(commentThreadIDs)):
            if(uniqueUsers[i]==users[k] and uniqueCommentThreadIDs[j]==commentThreadIDs[k]):
                involvement=involvement+1

        #initialArray[i][j]=involvement if involvement < 3 else min(2, involvement)
        initialArray[i][j]=1 if involvement >0 else 0
        #print (i*yDim+j)*100/totalLoops



initialMatrix= np.asmatrix(initialArray)
adjMatrix = initialMatrix.dot(initialMatrix.T)
print initialMatrix.shape
print initialMatrix
print adjMatrix.shape
print adjMatrix


adjMatrixDF = pd.DataFrame(data=adjMatrix, index=uniqueUsers,           columns=uniqueUsers)
A = adjMatrixDF.values
print("*****")
sum = np.sum(A,axis=1)
max = np.max(sum)
min = np.min(sum)
sum = (sum-min)/(max-min)
sumDF = pd.DataFrame(data=sum)


sumDF.hist()
plt.show()

print(A)

exit()




g = igraph.Graph.Adjacency((A > 0).tolist())

# Add edge weights and node labels.
g.es['weight'] = A[A.nonzero()]
#g.vs['label'] = uniqueUsers  # or a.index/a.columns


igraph.plot(g)