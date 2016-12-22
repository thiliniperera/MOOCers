from datetime import datetime
import pandas as pd
import csv
import numpy as np
from operator import attrgetter

#Video_code = ['i4x-HumanitiesandScience-StatLearning-video-de1971b8a61e45d584364679e5e07e55']
Video_code = ['i4x-Engineering-CS101-video-3f5301fa02fd4b60a541f1497eb3ff64']
file = 'videos/'+Video_code[0]+'.csv'

#reading video interaction file for video
df = pd.read_csv(file, parse_dates=True)
data = pd.DataFrame(df)
data['session_no'] = 1
header = list(data.columns.values)

#Create csv file to write data and add the headings
s = open('videos/sessionized_'+Video_code[0]+'.csv', 'w', newline='')
csv_session = csv.writer(s)
csv_session.writerow(header)

format = '%d-%m-%Y %I:%M:%S %p'
student_ids = data.anon_screen_name.unique()

j = 0
activity_list = []
#for each student create activity sequence
for student in student_ids:
    j += 1
    activity_list = data[data.anon_screen_name == student]
    activity_list['time'] = pd.to_datetime(activity_list['time'], format=format)
    activity_list = activity_list.sort_values(by='time') # First sort by time to prevent any discrepancies. Then by index to preserve the original order

    i = 1
    k = -1
    old_index = 0

    prev_time = activity_list['time'].iloc[0]
    for index, row in activity_list.iterrows():
        k += 1
        time_now = row['time']
        #time_difference = datetime.strptime(time_now, format)-datetime.strptime(prev_time, format)
        time_difference = time_now - prev_time
        prev_time = time_now

        if time_difference.total_seconds() > (30*60):
            activity_list.iloc[old_index:k, -1] = i #Last column is the session_no, -1 indicates last column
            i += 1
            activity_list.iloc[k:, -1] = i
            old_index = k
    activity_list['time'] = activity_list['time'].apply(lambda v: str(v))
    activity_list.to_csv(s, header=False, index=False)

    print(round((j / len(student_ids)) * 100, 2), "% completed")





