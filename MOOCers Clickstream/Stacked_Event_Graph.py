
from matplotlib import pyplot as plt
from datetime import datetime
import numpy as np
import csv

def movingaverage (values, window):
    weights = np.repeat(1.0, window)/window
    sma = np.convolve(values, weights, 'valid')
    return sma

f = open('C://Users//Kushan//Desktop//Fyp Data//Engineering_CS101_Summer2014//Engineering_CS101_Summer2014_VideoInteraction.csv')
csv_f = csv.reader(f)



Video = []
Unique_users = []
Datetimes = []
Event_type = []
Video_code = ['i4x-Engineering-CS101-video-z68']
for row in csv_f:
    if row[14] in Video_code:
        Video.append(row)
    if row[0] not in Event_type:
        Event_type.append(row[0])

Video = Video[1:]
Event_type = Event_type[1:]
count = 0;

# Make an array of x values
x = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]
# Make an array of y values for each x value
y_pause = np.zeros(20)
y_stop = np.zeros(20)
y_load = np.zeros(20)
y_seek = np.zeros(20)
y_speed_change = np.zeros(20)
y_play = np.zeros(20)


for row in Video:
    timeval = [datetime.strptime(row[10], "%M:%S.%f")]
    slot = round(timeval[0].minute / 3)
    if row[0] == 'pause_video':
        y_pause[slot-1] += 1
    elif row[0] == 'stop_video':
        y_stop[slot - 1] += 1
    elif row[0] == 'load_video':
        y_load[slot - 1] += 1
    elif row[0] == 'seek_video':
        y_seek[slot - 1] += 1
    elif row[0] == 'speed_change_video':
        y_speed_change[slot - 1] += 1
    elif row[0] == 'play_video':
        y_play[slot - 1] += 1

fig = plt.figure()
ax = fig.add_subplot(111)



ax.plot(x,y_pause,color="red",label="Pause")
ax.plot(x,y_stop,color="blue",label="Stop")
ax.plot(x,y_load,color="black",label="Load")
ax.plot(x,y_seek,color="green",label="Seek")
ax.plot(x,y_speed_change,color="purple",label="Speed Change")
ax.plot(x,y_play,color="orange",label="Play")

ax.set_title('Event chart')
ax.set_ylabel('Event count')
ax.set_xlabel('Time(Mins)')

print(count)
print(len(Unique_users)-1)
print(len(Video_code)-1)


plt.legend(loc='upper center', bbox_to_anchor=(0.5, 1.1),ncol=3)

plt.show()




