import numpy as np
from datetime import datetime
import csv
import pandas as pd

#Video_code = ['i4x-HumanitiesandScience-StatLearning-video-de1971b8a61e45d584364679e5e07e55']
Video_code = ['i4x-Engineering-CS101-video-3f5301fa02fd4b60a541f1497eb3ff64']
file = 'videos/sessionized_'+Video_code[0]+'.csv'

start_time = datetime.now()

# reading video interaction file for video
df = pd.read_csv(file, parse_dates=True)
data = pd.DataFrame(df)
header = data.columns.values

# Create csv file to write data and add the headings
s = open('sessions/session_'+Video_code[0]+'.csv', 'w', newline='')
csv_session = csv.writer(s)
session = ['session_id', 'user_id', 'NP', 'NB', 'NF', 'MP', 'SR','RL', 'AS', 'ES','TP', 'session_no']
csv_session.writerow(session);

# reading the unique student ids into a list
student_ids = data.anon_screen_name.unique()

i = 0
session_id = 0
no_of_removed_sessions = 0
# for each student create activity sequence
print("Total no of students: ",len(student_ids))
for student in student_ids:
    i += 1

    activity_list = data[data.anon_screen_name == student]
    activity_list['time'] = activity_list['time'].apply(lambda x: datetime.strptime(x, '%Y-%m-%d %H:%M:%S'))

    session_ids = data.session_no.unique()
    video_start_val = 0
    video_end_val = 0

    for session in session_ids:
        session_id += 1

        session_activity_list = activity_list[activity_list.session_no == session]
        playhead_positions = session_activity_list['video_current_time']
        temp_list = list(filter('None'.__ne__, playhead_positions))  # Removing None values
        cleaned_temp_list = [x for x in temp_list if str(x) != 'nan']  # Removing nan values

        if len(cleaned_temp_list) > 0:
            cleaned_temp_list = [float(i) for i in cleaned_temp_list]
            max_length = float(max(cleaned_temp_list))
            min_length = float(min(cleaned_temp_list))
            total_play_time = max_length - min_length

            if total_play_time < 100: # Remove sessions which lasted less than 100 seconds
                no_of_removed_sessions += 1
                continue
        else:
            no_of_removed_sessions += 1
            continue

        # proportion of skipped video content - SR
        seek_forward_list = session_activity_list.loc[(session_activity_list.event_type == 'seek_video') & (
        session_activity_list.video_new_time > session_activity_list.video_old_time)]
        seek_forward_list['SR'] = seek_forward_list['video_new_time'] - seek_forward_list['video_old_time']
        SR = seek_forward_list['SR'].sum()

        # replayed video length - RL (Sum of seek back events)

        seek_back_list = session_activity_list.loc[(session_activity_list.event_type == 'seek_video') & (
            session_activity_list.video_new_time < session_activity_list.video_old_time)]
        seek_back_list['RL'] = seek_back_list['video_old_time'] - seek_back_list['video_new_time']
        RL = seek_back_list['RL'].sum()

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

        # no of forward seeks and backward seeks - NB & NF
        NB = len(session_activity_list[(session_activity_list.event_type == 'seek_video') & (session_activity_list.video_new_time < session_activity_list.video_old_time)])
        NF = len(session_activity_list[(session_activity_list.event_type == 'seek_video') & (session_activity_list.video_new_time > session_activity_list.video_old_time)])

        session_list = []
        session_list.append(session_id)
        session_list.append(student)
        session_list.append(NP)
        session_list.append(NB)
        session_list.append(NF)
        session_list.append(MP)
        session_list.append(SR)
        session_list.append(RL)
        session_list.append(AS)
        session_list.append(ES)
        session_list.append(total_play_time)
        session_list.append(session)
        csv_session.writerow(session_list)


    print(round((i/len(student_ids))*100, 2), "% completed")

    '''
        w = 'C://Users//Kushan//Documents//MOOCers//MOOCers//MOOCers Clickstream//Clustering//Videos//'+(student)+'.csv'

        with open(w, 'w', newline='') as mycsvfile:
            thedatawriter = csv.writer(mycsvfile)
            thedatawriter.writerow(header)
            for index, row in activity_list.iterrows():
                thedatawriter.writerow(row)
    '''

print("Total no of students: ", len(student_ids))
print("Total no of sessions: ", session_id)
print("Total no of removed sessions: ", no_of_removed_sessions, " (", round((no_of_removed_sessions/session_id)*100, 2), "% of sessions removed)")

end_time = datetime.now()
print("Running time : ", end_time - start_time)















