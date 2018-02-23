from __future__ import division
import pandas as pd
import numpy as np
import os
import pickle
from sklearn.utils import shuffle
from sklearn.tree import DecisionTreeRegressor
from random import seed


def run(source, targets, reps, measure):
    print source
    data_family = {}
    for target in targets:
        train_content = pd.read_csv(source)
        train_content = shuffle(train_content)

        train_cols = train_content.columns.values.tolist()
        ctrain_indep = [c for c in train_cols if '<$' not in c]
        ctrain_dep = [c for c in train_cols if '<$' in c]
        assert (len(ctrain_dep) == 1), "Something is wrong"

        ctrain_dep = ctrain_dep[0]
        train_indep = train_content[ctrain_indep]
        train_dep = train_content[ctrain_dep]

        source_name = source.replace('../Data/', '').replace('.csv', '')
        target_name = target.replace('../Data/', '').replace('.csv', '')

        pickle_folder = './PickleLocker_' + source_name.split('_')[0] + '/'
        if not os.path.exists(pickle_folder):
            os.makedirs(pickle_folder)
        pickle_filename = pickle_folder + source_name + '|' + target_name + '|' + measure + '.p'

        data_family[source] = {}
        data_family[source][target] = {}
        data_family[source][target][measure] = []
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
                data_family[source][target][measure].append(l_ranks[ranks[0]])
            # for mmre based measures
            elif measure == 'mmre':
                test_indep = test_content[ctest_indep]
                test_dep = test_content[ctest_dep]
                test_predict_dep = tree.predict(test_indep)
                data_family[source][target][measure].append(np.mean(
                    [abs(actual - predicted) / actual for actual, predicted in zip(test_dep, test_predict_dep) if actual != 0]) * 100)
            # for abs based measures
            elif measure == 'abs_res':
                test_indep = test_content[ctest_indep]
                test_dep = test_content[ctest_dep]
                test_predict_dep = tree.predict(test_indep)
                data_family[source][target][measure].append(
                    sum([abs(actual - predicted) for actual, predicted in zip(test_dep, test_predict_dep)]))

        print data_family[source][target][measure]
        pickle.dump(data_family, open(pickle_filename, 'w'))


if __name__ == "__main__":
    seed(10)
    reps = 30
    familys = [ 'storm-obj1', 'storm-obj2', 'spear', 'sac',  'x264', 'sqlite',
                ]
    measures = ['rank', 'mmre', 'abs_res']
    data_folder = "../Data/"
    import multiprocessing as mp
    # Main control loop
    pool = mp.Pool()
    for family in familys:
        files = [data_folder + file for file in os.listdir(data_folder) if family in file]
        for measure in measures:
            for file in files:
                source = file
                targets = [f for f in files if file!=f]
                assert(len(targets) + 1 == len(files)), "Something is wrong"
                # run(source, targets, reps, measure)
                pool.apply_async(run, (source, targets, reps, measure))
            print
    pool.close()
    pool.join()
