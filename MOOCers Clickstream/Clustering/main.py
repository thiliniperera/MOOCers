import os

os.system('python VideoDataSeperator.py')
os.system('python "Session Reconstructor.py"')
os.system('python "Feature Calculator.py"')
os.system('python "Session Preprocessing.py"')
os.system('python kmedoidclustering.py')



