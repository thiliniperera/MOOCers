import pandas as pd
import numpy as np

from settings import Configurations

f = open(Configurations.InitialVideoInteractionFile[0])
Video_code = Configurations.Video_code
Video = pd.DataFrame()

chunksize = 1000000
for df in pd.read_csv(f, parse_dates=True, dtype={'video_old_speed': np.float64, 'video_new_speed': np.float64, 'video_old_time': np.float64,'video_new_time': np.float64},chunksize=chunksize):
    new_column_names = []
    for i in range(0, len(df.columns.values)):
        new_column_names.append(df.columns.values[i].replace("'", ""))
    df.columns = new_column_names

    Video = Video.append(df)
    print(len(Video))

Video_data = Video[Video['video_id'] == Video_code[0]]

print("Total Events: ",len(Video_data))
print ("Total unique users: ",len(Video_data.anon_screen_name.unique()))

print("Writing csv......")
w = ('videos/'+Video_code[0])+'.csv'
Video_data.to_csv(w, index=False)
