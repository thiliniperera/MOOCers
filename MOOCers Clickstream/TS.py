#libraries
import pandas as pd
import numpy as np
from pandas import Series, DataFrame, Panel
import matplotlib.pyplot as plt
Video_code = 'i4x-Engineering-CS101-video-z92'
#Video_code = [i4x-Engineering-CS101-video-eaf75029e92e4d1490533c55089bcb21]
Window_Size = 39

def smooth(x,window_len=Window_Size,window='hanning'):
    if x.ndim != 1:
        print("smooth only accepts 1 dimension arrays.")

    if x.size < window_len:
        print("Input vector needs to be bigger than window size.")

    if window_len < 3:
        return x

    if not window in ['flat', 'hanning', 'hamming', 'bartlett', 'blackman']:
        print("Window is on of 'flat', 'hanning', 'hamming', 'bartlett', 'blackman'")

    s = np.r_[x[window_len - 1:0:-1], x, x[-1:-window_len:-1]]
    # print(len(s))
    if window == 'flat':  # moving average
        w = np.ones(window_len, 'd')
    else:
        w = eval('np.' + window + '(window_len)')

    y = np.convolve(w / w.sum(), s, mode='valid')
    return y


url = 'C://Users//Kushan//Desktop//Fyp Data//Engineering_CS101_Summer2014//Engineering_CS101_Summer2014_VideoInteraction.csv'
#data loading
csv_data = pd.read_csv(url)
data = csv_data[csv_data['video_id'] == Video_code ]

#convert objects to float
data['video_current_time'] = data['video_current_time'].convert_objects(convert_numeric=True)

#removing rows with video current time NAN
data = data[np.isfinite(data['video_current_time'])]

#stat
Q1 = data.video_current_time.quantile(0.25)
Q3 = data.video_current_time.quantile(0.75)


IQR = Q3 - Q1
data = data[(data['video_current_time'])>= 0]
data = data[(data['video_current_time'])<= (Q3 + (1.5 *IQR))]

Max = data.video_current_time.max()
Min = data.video_current_time.min()

#histogram
#plt.hist(data.video_current_time, bins=100, normed=True)
#plt.show()

Max = int(round(Max))+1

x = []
x.extend(range(0,Max))
y_pause = np.zeros(Max)
y_stop = np.zeros(Max)
y_load = np.zeros(Max)
y_seek = np.zeros(Max)
y_speed_change = np.zeros(Max)
y_play = np.zeros(Max)

for row in data.values:
    if row[0] == 'pause_video':
        slot = int(round(row[2]));
        y_pause[slot] += 1
    elif row[0] == 'stop_video':
        slot = int(round(row[2]));
        y_stop[slot - 1] += 1
    elif row[0] == 'load_video':
        slot = int(round(row[2]));
        y_load[slot - 1] += 1
    elif row[0] == 'seek_video':
        slot_start = int(round(row[7]));
        y_seek[slot_start - 1] += 1
        slot_end = int(round(row[6]));
        y_seek[slot_end - 1] += 1
    elif row[0] == 'speed_change_video':
        slot = int(round(row[2]));
        y_speed_change[slot - 1] += 1
    elif row[0] == 'play_video':
        slot = int(round(row[2]));
        y_play[slot - 1] += 1

#manually setting initial and final values to 0
#y[0]= 0
#y[Max -1]= 0

#smoothing
y_pause_smooth = smooth(y_pause)
y_stop_smooth = smooth(y_stop)
y_load_smooth = smooth(y_load)
y_seek_smooth = smooth(y_seek)
y_speed_change_smooth = smooth(y_speed_change)
y_play_smooth = smooth(y_play)



x.extend(range(Max,Max+(Window_Size-1)))

#plt.plot(x,y_pause_smooth,color="red",label="Pause")
#plt.plot(x,y_play_smooth,color="orange",label="Play")
#plt.plot(x,y_load_smooth,color="black",label="Load")
#plt.plot(x,y_seek_smooth,color="green",label="Seek")
#plt.plot(x,y_speed_change_smooth,color="purple",label="Speed Change")
#plt.plot(x,y_stop_smooth,color="blue",label="Stop")

plt.title(Video_code)
plt.xlabel('Time(seconds)', fontsize=18)
plt.ylabel('Event count', fontsize=16)

plt.legend(loc='upper center')
plt.show()




