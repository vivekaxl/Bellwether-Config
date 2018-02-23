import os
import pickle
import numpy as np
import csv

pickle_folder = "./Pickle_Folder/"
myfile = open('./Results/overall.csv', 'w')
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

familys = ['x264', 'storm-obj2', 'storm-obj1', 'sac', 'spear']
heading = ['Parameters'] + familys
writer.writerow(heading)
parameters = ret.keys()

total_csv = []
for parameter in sorted(parameters):
    t = []
    for family in familys:
        t.append(ret[parameter][family])
    writer.writerow(t)

myfile.close()
print 'Done!'