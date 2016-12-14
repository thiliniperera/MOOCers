import numpy as np
from datetime import datetime, date
import csv
import pandas as pd
from operator import itemgetter
import itertools
Video_code = ['i4x-Engineering-CS101-video-z68']
file = 'C://Users//Kushan//Documents//MOOCers//MOOCers//MOOCers Clickstream//Clustering//Sessions//sessionized_'+Video_code[0]+'.csv'

#reading video interaction file for video
df = pd.read_csv(file, parse_dates=True)
data = pd.DataFrame(df)
header = data.columns.values

#Create csv file to write data and add the headings
s = open('C://Users//Kushan//Documents//MOOCers//MOOCers//MOOCers Clickstream//Clustering//Sessions//session.csv', 'w', newline='')
csv_session = csv.writer(s)
session = ['session_id','user_id', 'NP', 'NB', 'NF', 'MP', 'SR', 'AS', 'ES']
csv_session.writerow(session);

#reading the unique student ids into a list
student_ids = data.anon_screen_name.unique()

i = 0
session_id = 0
#for each student create activity sequence
for student in student_ids:
    i = i + 1

    activity_list = data[data.anon_screen_name == student]
    activity_list['time'] = activity_list['time'].apply(lambda x: datetime.strptime(x, '%Y-%m-%d %H:%M:%S'))
    activity_list = activity_list.sort_values(by='time')

    session_ids = data.session_no.unique()

    for session in session_ids:
        session_id += 1
        session_activity_list = activity_list[activity_list.session_no == session]

        # find the no of pauses - NP
        NP = len(session_activity_list[session_activity_list.event_type == 'pause_video'])

        # Median duration of pauses - MP
        pause_val = 0
        play_val = 0
        pause_detected = False

        pause_duration = []
        for index, row in session_activity_list.iterrows():
            if row['event_type'] == 'play_video':
                play_val = row['time']
                if pause_detected:
                    time_diff = play_val - pause_val
                    pause_duration.append(time_diff.total_seconds())
                    pause_detected = False
            elif row['event_type'] == 'pause_video':
                pause_val = row['time']
                pause_detected = True

        MP = np.median(pause_duration)

        # Average video speed(AS) and Effective speed change(ES)
        speed_change_list = session_activity_list.loc[(session_activity_list.event_type == 'speed_change_video')]
        new_weights = speed_change_list.video_new_speed.unique()
        old_weights = speed_change_list.video_old_speed.unique()
        weights = list(set(list(set(new_weights)) + list(set(old_weights))))

        if len(speed_change_list) > 0:
            starting_speed = speed_change_list.iloc[0, 5]
        else:
            starting_speed = 1

        if len(weights) > 0:
            AS = np.mean(weights)
        else:
            AS = 1

        ES = AS - starting_speed

        # proportion of skipped video content
        seek_forward_list = session_activity_list.loc[(session_activity_list.event_type == 'seek_video') & (session_activity_list.video_new_time > session_activity_list.video_old_time)]
        seek_forward_list['SR'] = seek_forward_list['video_new_time'] - seek_forward_list['video_old_time']
        SR = seek_forward_list['SR'].sum()

        # no of forward seeks and backward seeks
        NB = len(session_activity_list[(session_activity_list.event_type == 'seek_video') & (session_activity_list.video_new_time < session_activity_list.video_old_time)])
        NF = len(session_activity_list[(session_activity_list.event_type == 'seek_video') & (session_activity_list.video_new_time > session_activity_list.video_old_time)])

        session = []
        session.append(session_id)
        session.append(student)
        session.append(NP)
        session.append(NB)
        session.append(NF)
        session.append(MP)
        session.append(SR)
        session.append(AS)
        session.append(ES)
        csv_session.writerow(session)


    print(round((i/len(student_ids))*100, 2),"% completed")

    '''
    w = 'C://Users//Kushan//Documents//MOOCers//MOOCers//MOOCers Clickstream//Clustering//Videos//'+(student)+'.csv'

    with open(w, 'w', newline='') as mycsvfile:
        thedatawriter = csv.writer(mycsvfile)
        thedatawriter.writerow(header)
        for index, row in activity_list.iterrows():
            thedatawriter.writerow(row)
    '''














