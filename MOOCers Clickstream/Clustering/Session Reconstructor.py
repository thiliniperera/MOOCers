from datetime import datetime
import pandas as pd
import csv

Video_code = ['i4x-Engineering-CS101-video-z68']
file = 'C://Users//Kushan//Documents//MOOCers//MOOCers//MOOCers Clickstream//Clustering//Videos//'+Video_code[0]+'.csv'

#reading video interaction file for video
df = pd.read_csv(file, parse_dates=True)
data = pd.DataFrame(df)
data['session_no'] = 1
header = ['event_id'] + list(data.columns.values)

#Create csv file to write data and add the headings
s = open('C://Users//Kushan//Documents//MOOCers//MOOCers//MOOCers Clickstream//Clustering//Sessions//sessionized_'+Video_code[0]+'.csv', 'w', newline='')
csv_session = csv.writer(s)
csv_session.writerow(header)

student_ids = data.anon_screen_name.unique()

j = 0
activity_list = []
#for each student create activity sequence
for student in student_ids:
    j += 1
    activity_list = data[data.anon_screen_name == student]
    activity_list['time'] = activity_list['time'].apply(lambda x: datetime.strptime(x, '%M:%S.%f'))
    activity_list = activity_list.sort_values(by='time')

    i = 1
    k = -1
    old_index = 0

    prev_time = activity_list['time'].iloc[0]
    for index, row in activity_list.iterrows():
        k += 1
        time_now = row['time']
        time_difference = time_now-prev_time
        prev_time = time_now

        if time_difference.total_seconds() > (30*60):
            activity_list.iloc[old_index:k, -1] = i #Last column is the session_no, -1 indicates last column
            i += 1
            activity_list.iloc[k:, -1] = i
            #print(activity_list['session_no'])
            old_index = k
    activity_list.to_csv(s, header=False)

    print(round((j / len(student_ids)) * 100, 2), "% completed")




