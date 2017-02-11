import pandas as pd
import numpy as np
import csv

from resourses import Project_resourses

#import csv files
#file_activityGrade = open(Project_resourses.activityGradeFile)
#file_finalGrade = open(Project_resourses.finalGradeFile)

#read csv
#for df in pd.read_csv(file_activityGrade, parse_dates=True, dtype={})
#df = pd.read_csv(file_activityGrade)
#print(df)

import subprocess
subprocess.check_call(['Rscript', '../testing.R'], shell= False)