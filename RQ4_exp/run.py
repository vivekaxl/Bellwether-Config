from __future__ import division
import pandas as pd
import numpy as np
import os
import pickle
import sys
import random
from sklearn.utils import shuffle
from sklearn.tree import DecisionTreeRegressor
from random import seed
import copy


def run(files, no_rows, no_columns, percentage, loss):
    result_collector = {}
    contents = {}
    local_files = copy.copy(files)
    measurements = {}  # {file: indexes}

    for file in files:
        temp = pd.read_csv(file)
        temp = shuffle(temp)
        contents[file] = temp
        # constructor
        measurements[file] = []

    prev = sys.maxint
    loosy=loss
    gen = 1
    while True:
        result_collector[gen] = {}
        for file in local_files:
            # Get all indexes
            all_indexes = range(contents[file].shape[0])
            # remove which are already measured
            cleaned_indexes = [ind for ind in all_indexes if ind not in measurements[file]]
            assert(len(measurements[file]) + len(cleaned_indexes) == len(all_indexes)), "Something is wrong"
            random.shuffle(cleaned_indexes)
            # choose 1 training_coeff
            selected_indexes = cleaned_indexes[:no_columns]
            # add to measuerements
            measurements[file].extend(selected_indexes)
            assert(len(measurements[file]) == gen*no_columns), "Something is wrong"

        for file in local_files:
            result_collector[gen][file] = []
            source = file
            targets = [f for f in files if f != source]

            # Collect all the measured configurations of the file
            source_content = contents[file].ix[measurements[file]]
            # Get the columns
            source_cols = source_content.columns
            csource_indep = [c for c in source_cols if '<$' not in c]
            csource_dep = [c for c in source_cols if '<$' in c]
            assert (len(csource_dep) == 1), "Something is wrong"
            csource_dep = csource_dep[0]
            # Get the indep and dep columns
            source_indep = source_content[csource_indep]
            source_dep = source_content[csource_dep]
            # Fit the model
            model = DecisionTreeRegressor()
            model.fit(source_indep, source_dep)


            for target in targets:
                target_content = contents[target].ix[measurements[target]]
                target_cols = target_content.columns.tolist()
                ctarget_indep = [c for c in target_cols if '<$' not in c]
                ctarget_dep = [c for c in target_cols if '<$' in c]
                assert (len(ctarget_dep) == 1), "Something is wrong"
                ctarget_dep = ctarget_dep[0]

                target_content = target_content.sort(ctarget_dep)
                target_indep = target_content[ctarget_indep]
                target_dep = target_content[ctarget_dep]
                # Predict the target from the source model
                target_predict = model.predict(target_indep)

                # Take care of duplicate performance values
                l_ranks = np.searchsorted(np.sort(target_dep), target_dep).tolist()
                ranks = [i[0] for i in sorted(enumerate(target_predict), key=lambda x: x[1])]

                result_collector[gen][file].append(l_ranks[ranks[0]])

        if gen > 0:
            # eliminate files which are not possible bellwether
            temp = result_collector[gen]
            temp_split = [np.median(temp[key]) for key in temp.keys()]
            med = np.median(temp_split) + np.std(temp_split)
            temp_files = []
            for key, val in temp.iteritems():
                if np.median(val) <= med:
                    # print np.median(val), key
                    temp_files.append(key)
            local_files = copy.copy(temp_files)

            # print gen, len(local_files), loosy

        if prev <= len(local_files):
            loosy -= 1
        prev = min(prev, len(local_files))

        if len(measurements[local_files[0]]) > no_rows * percentage or loosy == 0:
            break
        gen += 1
    return local_files

def get_rd(family, detected_bws):
    data_folder = '../Data/'
    files = [data_folder + f for f in os.listdir(data_folder) if family in f ]
    files = [f for f in files if os.path.isfile(f)]
    ret_rd = []
    for detected_bw in detected_bws:
        rd_collector = []
        for target in files:
            if detected_bw == file: continue
            train_content = pd.read_csv(detected_bw)
            train_cols = train_content.columns.values.tolist()
            ctrain_indep = [c for c in train_cols if '<$' not in c]
            ctrain_dep = [c for c in train_cols if '<$' in c]
            assert (len(ctrain_dep) == 1), "Something is wrong"

            ctrain_dep = ctrain_dep[0]
            train_indep = train_content[ctrain_indep]
            train_dep = train_content[ctrain_dep]

            # Train a model using source data
            source_model = DecisionTreeRegressor()
            source_model.fit(train_indep, train_dep)

            # Read target data
            target_content = pd.read_csv(target)
            target_cols = target_content.columns.values.tolist()
            ctarget_indep = [c for c in target_cols if '<$' not in c]
            ctarget_dep = [c for c in target_cols if '<$' in c]
            assert (len(ctarget_dep) == 1), "Something is wrong"
            ctarget_dep = ctarget_dep[0]

            test_indep = target_content[ctarget_indep]
            test_dep = target_content[ctarget_dep]
            # Take care of duplicate performance values
            l_ranks = np.searchsorted(np.sort(test_dep), test_dep).tolist()

            target_test_predict_dep = source_model.predict(test_indep)

            ranks = [i[0] for i in sorted(enumerate(target_test_predict_dep), key=lambda x: x[1])]
            rd_collector.append(l_ranks[ranks[0]])
        ret_rd.append(np.median(rd_collector))
    return ret_rd


def run_main(step_size, percentage, loss):
    bellwethers = {
        'sac': ['sac_4'],
        'sqlite': ['sqlite_88'],
        'spear': ['spear_7', 'spear_1', 'spear_9'],
        'x264': ['x264_9', 'x264_10', 'x264_7','x264_1', 'x264_11', 'x264_8','x264_18', 'x264_6'],
        'storm-obj1': ['storm-obj1_feature6'],
        'storm-obj2': ['storm-obj2_feature7']
    }

    # seed(10)
    reps = 20
    familys = ['storm-obj1', 'storm-obj2','x264','spear', 'sac',    # 'sqlite',
               ]
    data_folder = "../Data/"
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
        'storm-obj1': 2049,
        'storm-obj2': 2049,
    }

    print '== ' * 20
    print step_size, percentage, loss

    collector = {}
    for family in familys:
        collector[family] = []
        files = [data_folder + file for file in os.listdir(data_folder) if family in file]
        files = [f for f in files if os.path.isfile(f)]
        count = 0
        for _ in xrange(reps):
            print ". ",
            ret = run(files, rows[family], step_size, percentage, loss)
            ret_rd = get_rd(family, ret)
            collector[family].append([ret, ret_rd])
            # print ret
            for bw in bellwethers[family]:
                if '../Data/' + bw + '.csv' in ret:
                    count += 1
                    print count,
                    break

        print
        print family, count
    print '== ' * 20

    import pickle
    pickle.dump(collector, open('./Pickle_Folder/experiment_pickle_' + str(step_size) + '_' + str(percentage)+ '_' + str(loss) + '.p', 'w'))

if __name__ == '__main__':
    step_sizes = [1, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20]
    percentages = [0.05, 0.07, 0.09, 0.1, 0.13, 0.15, 0.18, 0.2]
    losses = [3, 4, 5, 6, 7,]
    import multiprocessing as mp
    # Main control loop
    pool = mp.Pool()

    for step_size in step_sizes:
        for percentage in percentages:
            for loss in losses:
                pool.apply_async(run_main, (step_size, percentage, loss))

    pool.close()
    pool.join()