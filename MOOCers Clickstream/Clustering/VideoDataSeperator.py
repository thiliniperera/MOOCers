import pandas as pd
import numpy as np

from settings import Configurations

f = open(Configurations.InitialVideoInteractionFile[0])
df = pd.read_csv(f, parse_dates=True, dtype={'video_old_speed': np.float64, 'video_new_speed': np.float64})

for i in range(0,len(df.columns.values)):
    df.columns.values[i] = df.columns.values[i].replace("'", "")

Video_code = Configurations.Video_code
Video = df[df['video_id'] == Video_code[0]]


student_ids = np.random.choice(Video['anon_screen_name'].unique(), Configurations.NoOfUiniqueUsers, replace=False)
CoppedVideo = Video[Video['anon_screen_name'].isin(student_ids)]

print("Writing csv......")
w = ('videos/'+Video_code[0])+'.csv'
CoppedVideo.to_csv(w, index=False)