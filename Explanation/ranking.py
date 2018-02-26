import pandas as pd
from sklearn.tree import DecisionTreeRegressor
import os
import csv

data_folder = "../Data/"

familys = [ 'spear', 'sac',  'x264', 'storm-obj1', 'storm-obj2', 'sqlite',]
perc = 0.01
threshold = 2
result_folder = "./Ranks/"

collector = {}

for family in familys:
    collector[family] = {}
    files = [data_folder + f for f in os.listdir(data_folder) if family in f]
    files = sorted([f for f in files if os.path.isfile(f)])
    myFile = open(result_folder + family + '.csv', 'w')
    writer = csv.writer(myFile)
    heading = [" "] + files
    writer.writerow(heading)

    content_dict = {}
    for file in files:
        print "-- ", file
        target_content = pd.read_csv(file)
        cols = target_content.columns.values.tolist()
        ctrain_indep = [c for c in cols if '<$' not in c]
        ctarget_dep = [c for c in cols if '<$' in c]
        ctarget_dep = ctarget_dep[0]
        target_content = target_content.sort(ctarget_dep)
        d = {}
        for i, rowno in enumerate(target_content.index):
            indep = ','.join(map(str, target_content.iloc[rowno][ctrain_indep]))
            d[indep] = i

        content_dict[file] = d

    for source in files:
        t = [source]
        print source
        content = pd.read_csv(source)
        train_cols = content.columns.values.tolist()
        ctrain_indep = [c for c in train_cols if '<$' not in c]
        ctrain_dep = [c for c in train_cols if '<$' in c]
        assert (len(ctrain_dep) == 1), "Something is wrong"

        ctrain_dep = ctrain_dep[0]
        content = content.sort(ctrain_dep)
        rank1 = content.iloc[0][ctrain_indep]

        for target in files:
            if source == target:
                t.append(-1)
                continue
            else:
                t.append(content_dict[target][','.join(map(str, rank1))])
        writer.writerow(t)
        print t
    myFile.close()

print "Done!"
import pdb
pdb.set_trace()