import pickle
import numpy as np
import os
import csv


pickle_folder = "./PickleLocker/"

files = [pickle_folder + f for f in os.listdir(pickle_folder)]

seen = []
for file in files:
    content = pickle.load(open(file))
    sources = content.keys()
    for source in sources:
        myfile = open("./Results/" + source.split('/')[-1].replace('.csv', '.p') + ".csv", 'w')
        writer = csv.writer(myfile)
        heading = [' '] + map(str, [f*10 for f in range(1,11)])
        writer.writerow(heading)
        targets = content[source].keys()
        for target in targets:
            t = [target]
            percents = sorted(content[source][target].keys())
            for percent in percents:
                t.append(np.median(content[source][target][percent]))
            writer.writerow(t)
        myfile.close()

