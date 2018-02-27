import pickle
import os
import numpy as np

import csv

pickle_file = "./Processed/processed.p"

content = pickle.load(open(pickle_file, 'r'))

training_coeffs = [1, 2, 3, 4, 5, 6,]# 7, 8, 9, 10, ]#11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
familys = [ 'spear', 'sac',  'x264', 'storm-obj1', 'storm-obj2', 'sqlite']

rows = {
        'sac': 845,
        'sqlite': 1000,
        'spear': 16834,
        'x264': 2047,
        'storm-obj1': 536,
        'storm-obj2': 536,
    }

for family in familys:
    myfile = open('./Results/' + family + '_1.csv', 'w')
    writer = csv.writer(myfile)
    files = sorted(content[family][1].keys())
    heading = ['Source'] + map(str, [int(t*rows[family]*0.01) for t in training_coeffs])
    writer.writerow(heading)
    for training_coeff in training_coeffs:
        tt = []
        for source in files:
            t =  [source]
            for f in files:
                if not f == source:
                    t.extend(content[family][training_coeff][source][f])
            tt.append(t)
        
        
    myfile.close()

print 'Done!'