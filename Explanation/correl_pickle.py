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

    deps = {}
    tasks = sorted(common[common.keys()[0]].keys())
    assert(len(tasks) == no_of_tasks), "Something is wrong"
    for t in xrange(no_of_tasks):
        deps[tasks[t]] = []

    for i,key in enumerate(common.keys()):
        tasks = common[key].keys()
        for task in tasks:
            deps[task].append(common[key][task])

    print '= = ' * 20
    writer.writerow([family_name] + [len(deps[tasks[0]])])
    for stask in tasks:
        t = [stask]
        for ttask in tasks:
            if stask == ttask: t.append('X')
            else:
                t.append(round(corrcoef(deps[stask], deps[ttask])[1,0], 3))
        print
        writer.writerow(t)
myFile.close()