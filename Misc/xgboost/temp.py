import pandas as pd 
import os

files = [file for file in os.listdir('.') if '.csv' in file]

folders = ["./xgboost_obj1/", "./xgboost_obj2/", "./xgboost_obj3/"]

content_11 = pd.read_csv('configurations_xgboost11.csv')
content_12 = pd.read_csv('configurations_xgboost12.csv')
for file in files:
	if 'configurations' not in file:
		line = open(file).readline()
		print file, len(line.split(','))
		no_features = file.split('_')[-2]
		if no_features == '11':
			indep = content_11
		else:
			indep = content_12

		deps = pd.read_csv(file)
		cols = deps.columns
		assert(len(cols) == 4), "Something is wrong"

		for i, col in enumerate(cols[1:]):
			dep = deps[col]
			result = pd.concat([indep, dep], axis=1)
			result.to_csv(folders[i]+file, index=False)
print 'Done!'

