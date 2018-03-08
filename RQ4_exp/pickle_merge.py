import os
import pickle
import numpy as np
import csv

pickle_folder = "./PickleFolder/"
myfile = open('./Results_new/overall_normalized.csv', 'w')
writer = csv.writer(myfile)

ret = {}
files = [pickle_folder + f for f in os.listdir(pickle_folder) if '.p' in f]
for file in files:
    content = pickle.load(open(file))
    # assert(len(content.keys()) == 1), "Something is wrong"
    familys = content.keys()
    t_file = file.split('/')[-1].replace('experiment_pickle_', '').replace('.p', '')
    ret[t_file] = {}

    for family in familys:
        content_family = content[family]
        ret[t_file][family] = np.median([np.median(c[1]) for c in content_family])

rows = {
    'sac': 4000,
    'sqlite': 1000,
    'spear': 16834,
    'x264': 2047,
    'storm-obj1': 2049,
    'storm-obj2': 2049,
}

familys = ['x264', 'storm-obj2', 'storm-obj1', 'sac', 'spear', 'sqlite']
heading = ['step_size', 'percentage', 'loss'] + familys + ['N-'+family for family in familys]
writer.writerow(heading)
parameters = ret.keys()

total_csv = []
for parameter in sorted(parameters):
    t = parameter.split('_')
    tt = []
    for family in familys:
        t.append(ret[parameter][family])
        tt.append(ret[parameter][family] * 100/rows[family])
    writer.writerow(t + tt)

myfile.close()
print 'Done!'