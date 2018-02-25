import pandas as pd
from sklearn.tree import DecisionTreeRegressor
import os
import numpy as np

data_folder = "../Data/"

familys = [ 'spear', 'sac',  'x264', 'storm-obj1', 'storm-obj2', 'sqlite',]

collector = {}

for family in familys:
    files = [data_folder + f for f in os.listdir(data_folder) if family in f]
    files = [f for f in files if os.path.isfile(f)]

    collector = {}
    print files
    for file in files:
        print family, file
        content = pd.read_csv(file)
        train_cols = content.columns.values.tolist()
        ctrain_indep = [c for c in train_cols if '<$' not in c]
        ctrain_dep = [c for c in train_cols if '<$' in c]
        assert (len(ctrain_dep) == 1), "Something is wrong"

        ctrain_dep = ctrain_dep[0]

        lines = content.shape[0]
        for lineno in xrange(lines):
            print '. ',
            line = content.iloc[lineno]
            key = ','.join(map(str, line[ctrain_indep].tolist()))
            if key not in collector.keys():
                collector[key] = {}
            collector[key][file] = line[ctrain_dep]
        print

    import pickle
    pickle.dump(collector, open('pickle_folder/' + family + '_correl_pickle.p', 'w'))
