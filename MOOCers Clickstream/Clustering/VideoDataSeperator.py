import pandas as pd
import numpy as np

#f = open('C://Users//Kushan//Documents//Data//Chamil//HumanitiesandScience_StatLearning_Winter2015//HumanitiesandScience_StatLearning_Winter2015_VideoInteraction.csv')
f = open('C://Users//Kushan//Documents//Data//Data//Engineering_CS101_Summer2014//Engineering_CS101_Summer2014_VideoInteraction.csv')
df = pd.read_csv(f, parse_dates=True, dtype={'video_old_speed': np.float64, 'video_new_speed': np.float64})

#Video_code = ['i4x-HumanitiesandScience-StatLearning-video-de1971b8a61e45d584364679e5e07e55']
Video_code = ['i4x-Engineering-CS101-video-z68']
Video = df[df.video_id == Video_code[0]]

print("Writing csv......")
w = 'C://Users//Kushan//Documents//MOOCers//MOOCers//MOOCers Clickstream//Clustering//Videos//'+(Video_code[0])+'.csv'

Video.to_csv(w, index=False)