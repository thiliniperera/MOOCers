
from matplotlib import pyplot as plt
from datetime import datetime
import numpy as np
import pandas as pd
import csv

def reject_outliers(data):
    m = 2
    u = np.mean(data)
    s = np.std(data)
    filtered = [e for e in data if (u - 2 * s < e < u + 2 * s)]
    return filtered

def movingaverage (values, window):
    weights = np.repeat(1.0, window)/window
    sma = np.convolve(values, weights, 'valid')
    return sma

f = open('C://Users//Kushan//Desktop//Fyp Data//Engineering_CS101_Summer2014//Engineering_CS101_Summer2014_VideoInteraction.csv')
csv_f = csv.reader(f)

Video = []
Video_code = ['i4x-Engineering-CS101-video-z68']
for row in csv_f:
    if row[14] in Video_code:
        Video.append(row)

Header = Video[0]
Video.pop(0)

#print(pd.DataFrame(Video, columns=Header))


# Make an array of x values
x = []
x.extend(range(1,1001))
  # Make an array of y values for each x value
y = np.zeros(1000)
for row in Video:
    if row[0] == 'play_video' or row[0] == 'stop_video' or row[0] == 'load_video'  or row[0] == 'speed_change_video' or row[0] == 'play_video':
        if row[2] != "None":
            timeval = float(row[2])
            slot = round(timeval)
            y[slot - 1] += 1
y[999]=0
y[825:870]=0
y_MA = movingaverage(y,3)
print(len(x))
print(len(y))


plt.plot(x,y)
plt.show()




