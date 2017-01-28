import pandas as pd

from Settings import Configurations

initialFile = open(Configurations.InitialForumDataFile[0])

df = pd.read_csv(initialFile)
uniqueUsers = df['anon_screen_name'].unique()
comentThreadIDs =  df[df['type'] == 'CommentThread']['forum_post_id'].unique()

z = df['forum_post_id'].where(df['type'] == 'CommentThread', df['comment_thread_id'])

df['forum_id'] = z

initialMatrix = [[0 for x in range(len(comentThreadIDs))] for y in range(len(uniqueUsers))]

for i in range(len(uniqueUsers)):
    for j in range(len(comentThreadIDs)):
        initialMatrix[i][j]=1

