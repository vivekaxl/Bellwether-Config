from __future__ import division
import pandas as pd
import numpy as np
import os
import pickle
import random
from sklearn.utils import shuffle
from sklearn.tree import DecisionTreeRegressor
from random import seed


def run(files, no_rows, no_columns):
    evals = {}
    for file in files:
        content = pd.read_csv(file)
        content = shuffle(content)

        # Get indexes to split to train and testing data
        indexes = range(len(content))
        random.shuffle(indexes)
        train_indexes = indexes[:no_rows]

        # Get content based on the indexes generated
        selected_content = content.ix[train_indexes]

        evals[file] = selected_content

    return_dict = {}
    for file in evals.keys():

        source = evals[file]
        return_dict[file] = {}

        source_cols = source.columns.tolist()
        csource_indep = [c for c in source_cols if '<$' not in c]
        csource_dep = [c for c in source_cols if '<$' in c]
        assert (len(csource_dep) == 1), "Something is wrong"

        csource_dep = csource_dep[0]
        source_indep = source[csource_indep]
        source_dep = source[csource_dep]

        model = DecisionTreeRegressor()
        model.fit(source_indep, source_dep)

        targets = [eval for eval in evals.keys() if eval != file]
        for target in targets:
            target_content = evals[target]
            target_cols = target_content.columns.tolist()
            ctarget_indep = [c for c in target_cols if '<$' not in c]
            ctarget_dep = [c for c in target_cols if '<$' in c]
            assert (len(ctarget_dep) == 1), "Something is wrong"

            ctarget_dep = ctarget_dep[0]

            target_content = target_content.sort(ctarget_dep)
            target_indep = target_content[ctarget_indep]
            target_dep = target_content[ctarget_dep]

            target_predict = model.predict(target_indep)

            # Take care of duplicate performance values
            l_ranks = np.searchsorted(np.sort(target_dep), target_dep).tolist()

            ranks = [i[0] for i in sorted(enumerate(target_predict), key=lambda x: x[1])]
            return_dict[file][target] = [abs(target_dep.iloc[0] - target_dep.iloc[ranks[0]])*100]
            # print round(return_dict[file][target][-1], 3)



    return return_dict







if __name__ == "__main__":
    seed(10)
    reps = 20
    familys = [ 'sqlite', 'spear', 'sac',  'x264', 'storm-obj1', 'storm-obj2',
               ]
    data_folder = "../Data/"
    training_percents = range(1, 101)#11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
    columns = {
        'sac': 57,
        'sqlite': 14,
        'spear': 14,
        'x264': 16,
        'storm-obj1': 12,
        'storm-obj2': 12,
    }

    rows = {
        'sac': 845,
        'sqlite': 1000,
        'spear': 16834,
        'x264': 2047,
        'storm-obj1': 536,
        'storm-obj2': 536,
    }

    collector = {}
    for family in familys:
        print family
        collector[family] = {}
        files = [data_folder + file for file in os.listdir(data_folder) if family in file]
        files = [f for f in files  if  os.path.isfile(f)]
        print files
        for training_percent in training_percents:
            print training_percent,
            collector[family][training_percent] = None
            for rep in xrange(reps):
                print ' . ',
                temp_returns = run(files, int(training_percent*rows[family]/100), columns[family])
                if collector[family][training_percent] is None:
                    collector[family][training_percent] = temp_returns
                else:
                    temp_keys = temp_returns.keys()
                    assert(len(temp_keys) == len(collector[family][training_percent].keys())), "Something is wrong"
                    for temp_key in temp_keys:
                        temp_target_keys = temp_returns[temp_key]
                        for temp_target_key in temp_target_keys:
                            collector[family][training_percent][temp_key][temp_target_key].append(temp_returns[temp_key][temp_target_key][-1])

            print


    import pickle
    pickle.dump(collector, open('./Processed/processed_100.p', 'w'))

print "Done!"

