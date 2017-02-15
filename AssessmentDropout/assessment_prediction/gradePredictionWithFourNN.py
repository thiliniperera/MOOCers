import subprocess
from resourses import Project_resourses
import pandas as pd
import numpy as np
from sklearn.metrics import accuracy_score

scriptLocation = "../testing.R"

try:
    subprocess.check_call(['Rscript', scriptLocation], shell= False)
except :
    print "Script is not available"

#predicted_results = open(Project_resourses.gradePredictionResults)
#df = pd.read_csv('predicted_results')

df = pd.read_csv(Project_resourses.gradePredictionResults)
print df
y_true = 100*df['actual']
y_pred = 100*df['prediction'].round(2)

print y_true
print y_pred



accuracy = accuracy_score(y_true, y_pred , normalize=True, sample_weight=None)
#accuracy = 2
#print accuracy









