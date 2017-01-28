#from __future__ import division
import pandas as pd
import numpy as np

from Settings import Configurations

initialFile = open(Configurations.InitialForumDataFile[0])

df = pd.read_csv(initialFile, nrows=1000)
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

        initialArray[i][j]=involvement if involvement < 3 else min(2, involvement)
        #print (i*yDim+j)*100/totalLoops



initialMatrix= np.asmatrix(initialArray)
adjMatrix = initialMatrix.dot(initialMatrix.T)

print adjMatrix.shape
print adjMatrix

