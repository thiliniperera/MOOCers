import csv

f = open('C://Users//Kushan//Desktop//Fyp//Fyp Data//Engineering_CS101_Summer2014//Engineering_CS101_Summer2014_VideoInteraction.csv')
csv_f = csv.reader(f)


Video_code = ['i4x-Engineering-CS101-video-z68']
Video = []

for row in csv_f:
    if row[14] in Video_code:
        Video.append(row)

w = 'C://Users//Kushan//Documents//MOOCers//MOOCers//MOOCers Clickstream//Clustering//Videos//'+(Video_code[0])+'.csv'

with open(w, 'w', newline='') as mycsvfile:
    thedatawriter = csv.writer(mycsvfile)
    for row in Video:
        thedatawriter.writerow(row)
