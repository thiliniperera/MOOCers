import pandas as pd
import numpy as np
from numpy import *
from settings import Configurations

Video_code = Configurations.Video_code
file = 'results/'+Video_code[0]+'_kmedoid_results.csv'
grades = 'C://Users//Kushan//Documents//Data//Data//Engineering_CS101_Summer2014//Engineering_CS101_Summer2014_FinalGrade.csv'

df = pd.read_csv(file, parse_dates=True)
df_grades = pd.read_csv(grades,header=None,names = ["user_id", "course", "grade", "unknown"])
data = pd.DataFrame(df, columns=('user_id','NP', 'NB', 'NF', 'MP', 'SR', 'RL', 'AS', 'ES', 'cluster_label','TP','session_no'))

grades_values = pd.DataFrame(df_grades)

result = pd.merge(left=data,right=grades_values, left_on='user_id', right_on='user_id',how='left')

nan_positions = isnan(result['grade'])
result[nan_positions] = 0

result = result.drop('unknown', 1)
result = result.drop('course', 1)

cluster_0 = result[result.cluster_label == 0]
cluster_len_0 = len(cluster_0)
cluster_0 = np.mean(cluster_0)

cluster_1 = result[result.cluster_label == 1]
cluster_len_1 = len(cluster_1)
cluster_1 = np.mean(cluster_1)

cluster_2 = result[result.cluster_label == 2]
cluster_len_2 = len(cluster_2)
cluster_2 = np.mean(cluster_2)

cluster_3 = result[result.cluster_label == 3]
cluster_len_3 = len(cluster_3)
cluster_3 = np.mean(cluster_3)

cluster_4 = result[result.cluster_label == 4]
cluster_len_4 = len(cluster_4)
cluster_4 = np.mean(cluster_4)

cluster_5 = result[result.cluster_label == 5]
cluster_len_5 = len(cluster_5)
cluster_5 = np.mean(cluster_5)

df = pd.DataFrame([cluster_0, cluster_1, cluster_2, cluster_3, cluster_4, cluster_5])
df['no_of_sessions'] = [cluster_len_0,cluster_len_1,cluster_len_2,cluster_len_3,cluster_len_4,cluster_len_5]


print(df)

length = len(result)


