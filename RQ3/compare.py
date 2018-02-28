import pickle
import os
import numpy as np
import csv
from pdb import set_trace
from MiscUtils import Misc
from sk import sk_ranks, rdivDemo
from TransferLearners import Pooyan, Baseline, Waterloo


pickle_file = "./Processed/processed.p"

content = pickle.load(open(pickle_file, 'r'))

# 7, 8, 9, 10, ]#11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
# training_coeffs = [2, 4, 8, 16, 32, 64, 99]
training_coeffs = [100]
familys = ['sac', 'x264'] #, 'sqlite', 'sac', 'spear',  'x264', 'sqlite']

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
    files = sorted(content[family][2].keys())
    heading = ['Source'] + \
        map(str, [int(t * rows[family] * 0.01) for t in training_coeffs])
    writer.writerow(heading)
    print family
    print len(family)* "-"

    for training_coeff in training_coeffs:
        tt = []
        print "Sampled: {}%.".format(training_coeff)
        for source in files:
            t = [source]
            for f in files:
                if not f == source:
                    t.append(np.median(content[family][training_coeff][source][f]))
            tt.append(t)
        ranks = sk_ranks(tt)

        "Sort ranks"
        ranks = sorted(ranks, key=lambda x: x.rank)
        "Best rank"
        best_rank = Misc.uniques([x.rank for x in ranks])[0] 
        "Worst rank"
        worst_rank = Misc.uniques([x.rank for x in ranks])[-1]
        "Best dataset"
        best_dataset = [data.name for data in ranks if data.rank == best_rank]
        "Worst dataset"
        worst_dataset = [data.name for data in ranks if data.rank == worst_rank]
        "The remaining dataset"
        the_remaining = [data.name for data in ranks]# if best_rank < data.rank < worst_rank]
        

        "Compare the Transferring from the best/worst datasets on the rest"
        comp = []
        for best in best_dataset:
            comp_0 = [os.path.basename(best).rstrip(".csv")]
            for rest in the_remaining:
                if not rest == best:
                    comp_0.extend([waterloo(best, rest) for _ in xrange(30)])
            comp.append(comp_0)

        for worst in worst_dataset:
            comp_0 = [os.path.basename(worst).rstrip(".csv")]
            for rest in the_remaining:
                if not rest == worst:
                    comp_0.extend([waterloo(worst, rest) for _ in xrange(30)])
            comp.append(comp_0)

        rdivDemo(comp)
        print ""
    print 50*"===="
