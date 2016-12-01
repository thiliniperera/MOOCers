import csv
import pandas as pd
from pandas import DataFrame
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

file = 'C://Users//Kushan//Documents//MOOCers//MOOCers//MOOCers Clickstream//Clustering//Sessions//session.csv'

df = pd.read_csv(file, parse_dates=True)
dt = pd.DataFrame(df,columns=('user_id', 'NP', 'NB','NF'))

threedee = plt.figure().gca(projection='3d')
threedee.scatter(dt['NF'], dt['NP'], dt['NB'])
threedee.set_xlabel('NF')
threedee.set_ylabel('NP')
threedee.set_zlabel('NB')
plt.show()

