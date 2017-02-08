from __future__ import division
import pandas as pd
import numpy as np
import igraph
import matplotlib.pyplot as plt
import json as json

from Settings import Configurations

initialFile = open(Configurations.InitialForumDataFile[0])

df = pd.read_csv(initialFile,nrows = 100)
uniqueUsers = df['anon_screen_name'].unique()
print "Unique users: ",len(uniqueUsers)
users = df['anon_screen_name'].values
uniqueCommentThreadIDs =  df[df['type'] == 'CommentThread']['forum_post_id'].unique()
commentThreadIDs = df['forum_post_id'].where(df['type'] == 'CommentThread', df['comment_thread_id']).values

xDim= len(uniqueUsers)
yDim= len(uniqueCommentThreadIDs)
totalLoops = xDim*yDim

initialArray = [[0 for x in range(len(uniqueCommentThreadIDs))] for y in range(len(uniqueUsers))]

print "creating the matrix"
for i in range(len(uniqueUsers)):
    print i
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

adjMatrixDF = pd.DataFrame(data=adjMatrix, index=uniqueUsers,columns=uniqueUsers)
A = adjMatrixDF.values
g = igraph.Graph.Adjacency((A > 0).tolist(),mode = "undirected")
g.simplify()
g.es['weight'] = A[A.nonzero()]

nodes = pd.DataFrame(data=uniqueUsers, columns=['user_id'])
edge_list = g.get_edgelist()
degree_list = g.degree()
nodes['degree'] = degree_list
nodes['group'] =0

#community detection
cl = g.community_multilevel()
igraph.plot(g,"social_network"+Configurations.course+".png",vertex_color=[Configurations.color_list[x] for x in cl.membership])

index = 0
for row in cl:
    index += 1
    for item in row:
        nodes.set_value(item, 'group', index)

response = {'nodes':[],'links':[]}
for index, row in nodes.iterrows():
    user_id = row.user_id
    degree = row.degree
    group = row.group
    response['nodes'].append({'user_id': user_id, 'group' : group, 'degree' : degree})

for row in edge_list:
    source = row[0]
    target = row[1]
    weight = 1
    response['links'].append({'source': source, 'target': target, 'weight': weight})

with open('C://xampp//htdocs//lumino//graphFile.json', 'w') as fp:
    json.dump(response, fp)













sum = np.sum(A,axis=1)
graph = pd.DataFrame(data=sum, columns=['links'])
max = np.max(sum)
min = np.min(sum)
sum = (sum-min)/(max-min)
sumDF = pd.DataFrame(data=sum, columns=['score'])
#sumDF.hist()
#plt.show()


