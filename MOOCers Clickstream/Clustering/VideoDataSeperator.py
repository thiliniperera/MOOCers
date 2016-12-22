import pandas as pd
import numpy as np

from settings import Configurations

#f = open('C://Users//Kushan//Documents//Data//Chamil//HumanitiesandScience_StatLearning_Winter2015//HumanitiesandScience_StatLearning_Winter2015_VideoInteraction.csv')
f = open(Configurations.InitialVideoInteractionFile[0])
df = pd.read_csv(f, parse_dates=True, dtype={'video_old_speed': np.float64, 'video_new_speed': np.float64})

for i in range(0,len(df.columns.values)):
    df.columns.values[i] = df.columns.values[i].replace("'", "")

#Video_code = ['i4x-HumanitiesandScience-StatLearning-video-de1971b8a61e45d584364679e5e07e55']
Video_code = Configurations.Video_code
Video = df[df['video_id'] == Video_code[0]]

print("Writing csv......")
w = ('videos/'+Video_code[0])+'.csv'
Video.to_csv(w, index=False)