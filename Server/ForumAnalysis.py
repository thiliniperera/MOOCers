
import pandas as pd

student_course_csv = 'static/assets/student_course.csv'
student_course_df = pd.read_csv(student_course_csv)

eng_csv = 'static/assets/eng.csv'
eng_df = pd.read_csv(eng_csv)

hum_csv = 'static/assets/hum.csv'
hum_df = pd.read_csv(hum_csv)

course_1 = student_course_df[student_course_df['course']==0]

keys = course_1['name']
i1 = course_1.set_index(keys).index

keys2 = eng_df['anon_screen_name']
i2 = eng_df.set_index(keys2).index


# print course_1['name']
students_demo= eng_df[i2.isin(i1)]
course_2 = student_course_df[student_course_df['course']==1]

keys3 = course_2['name']
i3 = course_2.set_index(keys3).index

keys4 = hum_df['anon_screen_name']
i4 = hum_df.set_index(keys4).index


# print course_1['name']
student_demo2 = hum_df[i4.isin(i3)]
students_demo = students_demo.append(student_demo2 )

g = hum_df.groupby('anon_screen_name')

# df=g.count()
# print  df
print("Writing csv......")
w = ('static/assets/students_demo.csv')
students_demo.to_csv(w, index=False)