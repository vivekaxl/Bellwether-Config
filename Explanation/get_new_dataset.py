import pickle
import os
from numpy import corrcoef
import csv

folder = "./pickle_folder/"
data_folder = "../Data/"
myFile = open('correl.csv', 'w')
writer = csv.writer(myFile)

files = [folder + f for f in os.listdir(folder) if '.p' in f]


for file in files:
    family_name = file.split('/')[-1].split('_')[0]
    tfiles = [data_folder + f for f in os.listdir(data_folder) if family_name in f]
    tfiles = [f for f in tfiles if os.path.isfile(f)]
    no_of_tasks = len(tfiles)

    content = pickle.load(open(file))
    common = {}
    keys = content.keys()
    for key in keys:
        if len(content[key]) == no_of_tasks:
            common[key] = content[key]

    indeps = common.keys()
    diff_tasks = common[common.keys()[0]].keys()
    for diff_task in diff_tasks:
        deps = []
        for indep in indeps:
            deps.append(common[indep][diff_task])
        assert(len(indeps) == len(deps)), "Somethign is wrong"

        heading = ['f'+str(i) for i in xrange(len(indeps))] + ['<$d1']

    import pdb
    pdb.set_trace()

