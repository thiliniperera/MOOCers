from __future__ import division
import pandas as pd
import numpy as np
import igraph
import matplotlib.pyplot as plt
import json as json

from Settings import Configurations

initialFile = open(Configurations.InitialForumDataFile[0])

df = pd.read_csv(initialFile,nrows =500)
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

degree_df = pd.DataFrame(data=degree_list, columns=['links'])
max = np.max(degree_list)
min = np.min(degree_list)
score = (degree_list-min)/(max-min)
nodes['score'] = score
scoreDF = pd.DataFrame(data=score, columns=['score'])

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
    score = row.score
    response['nodes'].append({'user_id': user_id, 'group' : group, 'degree' : degree, 'score' : score})

for row in edge_list:
    source = row[0]
    target = row[1]
    weight = 1
    response['links'].append({'source': source, 'target': target, 'weight': weight})

with open('C://Users//Kushan//Documents//FYP Jan//MOOCers//Server//static//assets//nodes.json', 'w') as fp:
    json.dump(response, fp)

scoreDF.hist()
plt.show()


GradesFile = open(Configurations.Grades[0])
df_grades = pd.read_csv(GradesFile, header=None, names=["user_id", "course", "grade", "unknown"])
grades_values = pd.DataFrame(df_grades)
result = pd.merge(left=nodes, right=grades_values, left_on='user_id', right_on='user_id', how='left')

result = result.drop('unknown', 1)
result = result.drop('course', 1)

print "Grade null" , len(result) - result['grade'].count()
result['grade'].fillna(0, inplace=True)
grade_mean = result.groupby(['group']).mean()
varience = result.groupby(['group']).var()


print "Mean", grade_mean
print "Varience" ,varience