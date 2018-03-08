import pickle
import os
import numpy as np

import csv

pickle_file = "./Processed/processed.p"

content = pickle.load(open(pickle_file, 'r'))

familys = ['sac', 'sqlite',  'x264', 'spear']
training_coeffs = [1, 2, 3, 4, 5, 6, 7, 8, 9]

for family in familys:
    myfile = open('./Results_10-100/' + family + '_form2.csv', 'w')
    writer = csv.writer(myfile)
    files = sorted(content[family][1].keys())
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