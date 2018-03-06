from __future__ import division
import pandas as pd
import numpy as np
import os
import pickle
import random
from sklearn.utils import shuffle
from sklearn.tree import DecisionTreeRegressor
from random import seed

def run(source, targets, reps, measure, perc=0.4):
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
        pickle_filename = pickle_folder + source_name + '|' + target_name + '|' + measure + '|' + str(int(perc * 100)) + '.p'

        data_family[source] = {}
        data_family[source][target] = {}
        data_family[source][target][perc] = {}
        data_family[source][target][perc][measure] = {}
        data_family[source][target][perc][measure]['bellwether'] = []
        data_family[source][target][perc][measure]['target'] = []

        # Read target data
        target_content = pd.read_csv(target)
        target_cols = target_content.columns.values.tolist()
        ctarget_indep = [c for c in target_cols if '<$' not in c]
        ctarget_dep = [c for c in target_cols if '<$' in c]
        assert (len(ctarget_dep) == 1), "Something is wrong"
        ctarget_dep = ctarget_dep[0]

        for _ in xrange(reps):
            print ". ",
            # Train a model using source data
            source_model = DecisionTreeRegressor()
            source_model.fit(train_indep, train_dep)

            # Get indexes to split to train and testing data
            indexes = range(len(target_content))
            random.shuffle(indexes)

            # Get training and testing indexes to split into train and test
            target_train_indexes = indexes[:int(len(target_content) * perc)]
            target_test_indexes = indexes[int(len(target_content) * perc):]

            # Get content based on the indexes generated
            target_train_content = target_content.ix[target_train_indexes]
            target_test_content = target_content.ix[target_test_indexes]

            # Get train and test dep and indep
            target_train_indep = target_train_content[ctarget_indep]
            target_train_dep = target_train_content[ctarget_dep]

            # Train target model using perc amount of training data
            target_model = DecisionTreeRegressor()
            target_model.fit(target_train_indep, target_train_dep)

            # for rank based measures
            if measure == 'rank':
                test_content = target_test_content.sort(ctarget_dep)
                test_indep = test_content[ctarget_indep]
                test_dep = test_content[ctarget_dep]

                source_test_predict_dep = source_model.predict(test_indep)
                # Take care of duplicate performance values
                l_ranks = np.searchsorted(np.sort(test_dep), test_dep).tolist()

                ranks = [i[0] for i in sorted(enumerate(source_test_predict_dep), key=lambda x: x[1])]
                data_family[source][target][perc][measure]['bellwether'].append(abs(test_dep.iloc[0] - test_dep.iloc[ranks[0]])*100)

                target_test_predict_dep = target_model.predict(test_indep)
                ranks = [i[0] for i in sorted(enumerate(target_test_predict_dep), key=lambda x: x[1])]
                data_family[source][target][perc][measure]['target'].append(abs(test_dep.iloc[0] - test_dep.iloc[ranks[0]])*100)

            elif measure == 'mmre':
                test_indep = target_test_content[ctarget_indep]
                test_dep = target_test_content[ctarget_dep]

                source_test_predict_dep = source_model.predict(test_indep)
                data_family[source][target][perc][measure]['bellwether'].append(np.mean(
                    [abs(actual - predicted) / actual for actual, predicted in zip(test_dep, source_test_predict_dep) if
                     actual != 0]) * 100)

                target_test_predict_dep = target_model.predict(test_indep)
                data_family[source][target][perc][measure]['target'].append(np.mean(
                    [abs(actual - predicted) / actual for actual, predicted in zip(test_dep, target_test_predict_dep) if
                     actual != 0]) * 100)
            elif measure == 'abs_res':
                test_indep = target_test_content[ctarget_indep]
                test_dep = target_test_content[ctarget_dep]

                source_test_predict_dep = source_model.predict(test_indep)
                data_family[source][target][perc][measure]['bellwether'].append(
                    sum([abs(actual - predicted) for actual, predicted in zip(test_dep, source_test_predict_dep)]))

                target_test_predict_dep = target_model.predict(test_indep)
                data_family[source][target][perc][measure]['target'].append(
                    sum([abs(actual - predicted) for actual, predicted in zip(test_dep, target_test_predict_dep)]))

        pickle.dump(data_family, open(pickle_filename, 'w'))


if __name__ == "__main__":
    seed(10)
    reps = 40
    familys = [
         'sac',#'sqlite', #'spear', 'x264','storm-obj1', 'storm-obj2','sac',
                ]
    measures = ['rank']#, 'mmre', 'abs_res']
    percs = [ .15, .20, .05, .10, .25, .30, .35, .40]
    data_folder = "../Data/"
    bellwethers = {
        'sac': 'sac_4',
        'sqlite': 'sqlite_17',
        'spear': 'spear_7',
        'x264': 'x264_9',
        'storm-obj1': 'storm-obj1_feature8',
        'storm-obj2': 'storm-obj2_feature9'
    }
    import multiprocessing as mp
    # Main control loop
    pool = mp.Pool()
    for family in familys:
        files = [data_folder + file for file in os.listdir(data_folder) if family in file]
        for measure in measures:
            for perc in percs:
                    source = data_folder + bellwethers[family] + '.csv'
                    targets = [f for f in files if f!=source]
                    print source
                    print targets
                    assert(len(targets) + 1 == len(files)), "Something is wrong"
                    run(source, targets, reps, measure, perc)
                    # pool.apply_async(run, (source, targets, reps, measure, perc))
    pool.close()
    pool.join()