import csv
f = open('C://Users//Kushan//Desktop//Fyp Data//Engineering_CS101_Summer2014//Engineering_CS101_Summer2014_VideoInteraction.csv')
csv_f = csv.reader(f)

Video_code = []
for row in csv_f:
    if row[14] not in Video_code :
        Video_code.append(row[14])

print(Video_code)
