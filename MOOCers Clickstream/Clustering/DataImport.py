import numpy as np
from datetime import datetime, date
import csv
import pandas as pd
from operator import itemgetter
import itertools
Video_code = ['i4x-Engineering-CS101-video-z68']
file = 'C://Users//Kushan//Documents//MOOCers//MOOCers//MOOCers Clickstream//Clustering//Videos//'+Video_code[0]+'.csv'

#reading video interaction file for video
df = pd.read_csv(file, parse_dates=True)
data = pd.DataFrame(df)

#Create csv file to write data and add the headings
s = open('C://Users//Kushan//Documents//MOOCers//MOOCers//MOOCers Clickstream//Clustering//Sessions//session.csv', 'w', newline='')
csv_session = csv.writer(s)
session = ['user_id', 'NP', 'NB', 'NF', 'MP', 'SR']
csv_session.writerow(session);

#reading the unique student ids into a list
student_ids = data.anon_screen_name.unique()

i = 0
#for each student create activity sequence
for student in student_ids:
    i = i + 1

    activity_list = data[data.anon_screen_name == student]
    activity_list['time'] = activity_list['time'].apply(lambda x: datetime.strptime(x, '%M:%S.%f'))
    activity_list = activity_list.sort_values(by='time')


    prev_time = activity_list['time'].iloc[0]
    for index, row in activity_list.iterrows():
        time_now = row['time']
        time_difference = time_now-prev_time
        prev_time = time_now

        if time_difference.total_seconds() >(30*60):
            activity_list = activity_list[:index]


    #find the no of pauses NP
    NP = len(activity_list[activity_list.event_type == 'pause_video'])

    pause_val = 0
    play_val = 0
    pause_detected = False

    #Median duration of pauses

    pause_duration = []
    for index, row in activity_list.iterrows():
        if row['event_type'] == 'play_video':
            play_val = row['time']
            if pause_detected:
                #play_val = datetime.strptime(play_val, "%M:%S.%f")
                #pause_val = datetime.strptime(pause_val, "%M:%S.%f")
                time_diff = play_val - pause_val
                if time_diff.total_seconds() < 0:
                    print(student)
                    print(play_val)
                    print(pause_val)
                pause_duration.append(time_diff.total_seconds())
                pause_detected = False
        elif row['event_type'] == 'pause_video':
            pause_val = row['time']
            pause_detected = True

    MP = np.median(pause_duration)

    #proportion of skipped video content

    seek_forward_list = activity_list.loc[(activity_list.event_type == 'seek_video') & (activity_list.video_new_time > activity_list.video_old_time)]

    seek_forward_list['SR'] = seek_forward_list['video_new_time'] - seek_forward_list['video_old_time']

    SR = seek_forward_list['SR'].sum()

    #no of forward seeks and backward seeks
    NB = len(activity_list[(activity_list.event_type == 'seek_video') & (activity_list.video_new_time < activity_list.video_old_time)])
    NF = len(activity_list[(activity_list.event_type == 'seek_video') & (activity_list.video_new_time > activity_list.video_old_time)])

    session = []
    session.append(student)
    session.append(NP)
    session.append(NB)
    session.append(NF)
    session.append(MP)
    session.append(SR)
    csv_session.writerow(session)

    print((i/len(student_ids))*100)

    '''
    w = 'C://Users//Kushan//Documents//MOOCers//MOOCers//MOOCers Clickstream//Clustering//Videos//'+(student)+'.csv'
    print(student)

    with open(w, 'w', newline='') as mycsvfile:
        thedatawriter = csv.writer(mycsvfile)
        for index, row in activity_list.iterrows():
            thedatawriter.writerow(row)
    '''














