import pickle
import os
import numpy as np

import csv

pickle_file = "./Processed/processed_4.p"

content = pickle.load(open(pickle_file, 'r'))

familys = ['sqlite', ]#'sac', 'x264', 'spear']
training_coeffs = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
rows = {
        'sac': 845,
        'sqlite': 1000,
        'spear': 16834,
        'x264': 2047
    }

for family in familys:
    myfile = open('./Results_3/' + family + '_form4.csv', 'w')
    writer = csv.writer(myfile)
    files = sorted(content[family][1].keys())
    heading = ['Source'] + map(str, [int(t*rows[family]*0.01) for t in training_coeffs])
    writer.writerow(heading)
    for source in files:
        tt = [source]
        for training_coeff in training_coeffs:
            t =  []
            for f in files:
                if f == source: pass
                else:
                    t.append(np.median(content[family][training_coeff][source][f]))
            tt.append(np.median(t))
        writer.writerow(tt)
    myfile.close()

print 'Done!'