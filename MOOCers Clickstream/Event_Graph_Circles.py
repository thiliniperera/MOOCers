import numpy as np
import pylab as pl
from matplotlib import pyplot as plt
from datetime import time, datetime


import numpy as np
import csv
f = open('C://Users//Kushan//Desktop//Fyp Data//Engineering_CS101_Summer2014//Engineering_CS101_Summer2014_VideoInteraction.csv')
csv_f = csv.reader(f)

Video = []
Datetimes = []
Event_type = []
Video_code = ['i4x-Engineering-CS101-video-z68']
for row in csv_f:
    if row[14] in Video_code :
        Video.append(row)
    if row[0] not in Event_type:
        Event_type.append(row[0])

Video = Video[1:]
Event_type = Event_type[1:]

print(Event_type)

# Make an array of x values
x = []
# Make an array of y values for each x value
y1,y2,y3,y4,y5,y6 = [],[],[],[],[],[]
Datetimes = []

for row in Video:
    Datetimes.append([datetime.strptime(row[10], "%M:%S.%f")])
    #x.append(row[10])
    if row[0] == 'pause_video':
        y1.append(1)
        y2.append(0)
        y3.append(0)
        y4.append(0)
        y5.append(0)
        y6.append(0)
    elif row[0] == 'stop_video':
        y1.append(0)
        y2.append(2)
        y3.append(0)
        y4.append(0)
        y5.append(0)
        y6.append(0)
    elif row[0] == 'load_video':
        y1.append(0)
        y2.append(0)
        y3.append(3)
        y4.append(0)
        y5.append(0)
        y6.append(0)
    elif row[0] == 'seek_video':
        y1.append(0)
        y2.append(0)
        y3.append(0)
        y4.append(4)
        y5.append(0)
        y6.append(0)
    elif row[0] == 'speed_change_video':
        y1.append(0)
        y2.append(0)
        y3.append(0)
        y4.append(0)
        y5.append(5)
        y6.append(0)
    elif row[0] == 'play_video':
        y1.append(0)
        y2.append(0)
        y3.append(0)
        y4.append(0)
        y5.append(0)
        y6.append(6)

Datetimes_a = np.asarray(Datetimes)
y1_a = np.asarray(y1)
y2_a = np.asarray(y2)
y3_a = np.asarray(y3)
y4_a = np.asarray(y4)
y5_a = np.asarray(y5)
y6_a = np.asarray(y6)

fig = plt.figure()
ax = fig.add_subplot(111)

ax.plot(Datetimes_a,y1_a,'o',color="red")
ax.plot(Datetimes_a,y2_a,'o',color="blue")
ax.plot(Datetimes_a,y3_a,'o',color="black")
ax.plot(Datetimes_a,y4_a,'o',color="green")
ax.plot(Datetimes_a,y5_a,'o',color="yellow")
ax.plot(Datetimes_a,y6_a,'o',color="orange")
#ax.fill_between(Datetimes_a, y1_a, color='grey', alpha='0.5')

ax.set_title('100 % stacked area chart')
ax.set_ylabel('Percent (%)')
ax.margins(0, 0) # Set margins to avoid "whitespace"

plt.show()







