import pandas as pd
from sklearn.tree import DecisionTreeRegressor
import os
import numpy as np

data_folder = "../Data/"

familys = [ 'spear', 'sac',  'x264', 'storm-obj1', 'storm-obj2', 'sqlite',]
perc = 0.01
threshold = 4

collector = {}

for family in familys:
    collector[family] = {}
    files = [data_folder + f for f in os.listdir(data_folder) if family in f]
    files = [f for f in files if os.path.isfile(f)]

    for file in files:
        print file
        content = pd.read_csv(file)
        train_cols = content.columns.values.tolist()
        ctrain_indep = [c for c in train_cols if '<$' not in c]
        ctrain_dep = [c for c in train_cols if '<$' in c]
        assert (len(ctrain_dep) == 1), "Something is wrong"

        ctrain_dep = ctrain_dep[0]
        content = content.sort(ctrain_dep)
        indexes = range(len(content))
        selected_indexes = indexes[:int(len(indexes) * perc)]
        selected_content = content.ix[selected_indexes]

        train_indep = content[ctrain_indep]
        train_dep = range(train_indep.shape[0])


        model = DecisionTreeRegressor()
        model.fit(train_indep, train_dep)

        feature_importance = model.feature_importances_
        columns = content.columns

        ranked_order = sorted(zip(columns, feature_importance), key=lambda x: x[1], reverse=True)[:threshold]

        collector[family][file] = [x[0] for x in ranked_order]

import pickle
pickle.dump(collector, open('feature_imp.p', 'w'))
