from __future__ import division
import pandas as pd
import numpy as np
import os
import pickle
from sklearn.utils import shuffle
from sklearn.tree import DecisionTreeRegressor
from random import seed
import random


def run(source, targets, reps, measure, percent):
    print source
    data_family = {}
    for target in targets:
        train_content = pd.read_csv(source)
        train_content = shuffle(train_content)

        train_cols = train_content.columns.values.tolist()
        ctrain_indep = [c for c in train_cols if '<$' not in c]
        ctrain_dep = [c for c in train_cols if '<$' in c]
        assert (len(ctrain_dep) == 1), "Something is wrong"

        # Get indexes to split to train and testing data
        indexes = range(len(train_content))
        random.shuffle(indexes)

        # Get training and testing indexes to split into train and test
        target_train_indexes = indexes[:int(len(train_content) * percent * 0.01)]

        train_content = train_content.ix[target_train_indexes]

        ctrain_dep = ctrain_dep[0]
        train_indep = train_content[ctrain_indep]
        temp_train = train_content[ctrain_dep]
        train_dep = (temp_train - temp_train.min())/(temp_train.max() - temp_train.min())

        source_name = source.replace('../../Data/', '').replace('.csv', '')
        target_name = target.replace('../../Data/', '').replace('.csv', '')

        pickle_folder = './PickleLocker_' + source_name.split('_')[0] + '/'
        if not os.path.exists(pickle_folder):
            os.makedirs(pickle_folder)
        pickle_filename = pickle_folder + source_name + '|' + target_name + '|' + str(percent) + '.p'

        data_family[source] = {}
        data_family[source][target] = {}
        data_family[source][target][percent] = []
        for _ in xrange(reps):
            print ". ",
            tree = DecisionTreeRegressor()
            tree.fit(train_indep, train_dep)

            test_content = pd.read_csv(target)
            test_cols = test_content.columns.values.tolist()
            ctest_indep = [c for c in test_cols if '<$' not in c]
            ctest_dep = [c for c in test_cols if '<$' in c]
            assert (len(ctest_dep) == 1), "Something is wrong"
            ctest_dep = ctest_dep[0]

            assert(len(ctrain_indep) == len(ctest_indep)), "Somethign is wrong"

            # for rank based measures
            if measure == 'rank':
                test_content = test_content.sort(ctest_dep)
                test_indep = test_content[ctest_indep]
                test_dep = test_content[ctest_dep]
                test_predict_dep = tree.predict(test_indep)
                # Take care of duplicate performance values
                l_ranks = np.searchsorted(np.sort(test_dep), test_dep).tolist()
                ranks = [i[0] for i in sorted(enumerate(test_predict_dep), key=lambda x:x[1])]
                data_family[source][target][percent].append(abs(test_dep.iloc[0] - test_dep.iloc[ranks[0]])*100)
                # print test_dep.iloc[0], test_dep.iloc[ranks[0]], abs(test_dep.iloc[0] - test_dep.iloc[ranks[0]])

        print data_family[source][target][percent]
        pickle.dump(data_family, open(pickle_filename, 'w'))


if __name__ == "__main__":
    seed(10)
    reps = 30
    familys = [ 'sqlite', 'storm-obj1', 'storm-obj2', 'spear', 'sac',  'x264',
                ]
    measures = [ 'rank',]#'mmre', 'abs_res',
    percents = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
    data_folder = "../../Data/"
    import multiprocessing as mp
    # Main control loop
    pool = mp.Pool()
    for family in familys:
        files = [data_folder + file for file in os.listdir(data_folder) if family in file]
        for measure in measures:
            for percent in percents:
                for file in files:
                    source = file
                    targets = [f for f in files if file!=f]
                    assert(len(targets) + 1 == len(files)), "Something is wrong"
                    # run(source, targets, reps, measure, percent)
                    pool.apply_async(run, (source, targets, reps, measure, percent))
                print
    pool.close()
    pool.join()
