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


def run(files, no_rows, no_columns):
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
    loosy=4
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

                target_content = target_content.sort_values(by=ctarget_dep)
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

        if len(measurements[local_files[0]]) > no_rows * 0.08 or loosy == 0:
            break
        gen += 1
    return local_files

if __name__ == "__main__":
    bellwethers = {
        'sac': ['sac_4'],
        'sqlite': ['sqlite_88'],
        'spear': ['spear_7', 'spear_1', 'spear_9'],
        'x264': ['x264_9', 'x264_10', 'x264_7','x264_1', 'x264_11', 'x264_8','x264_18', 'x264_6'],
        'storm-obj1': ['storm-obj1_feature6'],
        'storm-obj2': ['storm-obj2_feature7']
    }

    seed(10)
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

    collector = {}
    for family in familys:
        collector[family] = {}
        files = [data_folder + file for file in os.listdir(data_folder) if family in file]
        files = [f for f in files if os.path.isfile(f)]
        count = 0
        for _ in xrange(20):
            print ". ",
            ret = run(files, rows[family], 7)
            # print ret
            for bw in bellwethers[family]:
                if '../Data/' + bw + '.csv' in ret:
                    count += 1
                    print count,
                    break

        print
        print family, count
        print '== ' * 20
