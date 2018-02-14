import pickle
import os
import numpy as np

import csv

pickle_file = "./Processed/processed.p"

content = pickle.load(open(pickle_file, 'r'))

familys = ['sac', 'sqlite',  'x264', 'spear']
training_coeffs = [1, 2, 3, 4, 5, 6, 7, 8, 9]

for family in familys:
    myfile = open('./Results/' + family + '.csv', 'w')
    writer = csv.writer(myfile)
    for training_coeff in training_coeffs:
        files = sorted(content[family][training_coeff].keys())
        # myfile = open('./Results/' + family + '_' + str(training_coeff) + '.csv', 'w')
        # writer = csv.writer(myfile)
        heading = ['Source'] + files
        writer.writerow(heading)
        for source in files:
            t =  [source]
            for f in files:
                if f == source: t.append('X')
                else:
                    t.append(np.median(content[family][training_coeff][source][f]))
            writer.writerow(t)
        writer.writerow(['='*30])
    myfile.close()

print 'Done!'