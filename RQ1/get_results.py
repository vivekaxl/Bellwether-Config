import pickle
import os
import numpy as np
import csv

pickle_folder = './Processed/'
measures = ['rank',]# 'mmre', 'abs_res']
files = [pickle_folder+file for file in os.listdir(pickle_folder) if '.p' in file]
result_folder = './Results_10-100/'
for file in files:
    system_name = file.split('/')[-1].split('.p')[0]
    for measure in measures:
        myFile = open(result_folder + 'normalized-'+system_name + '_' + measure + '.csv', 'w')
        writer = csv.writer(myFile)
        d = pickle.load(open(file))
        sources = d.keys()
        heading =  ['Target '] + sorted(sources)
        writer.writerow(heading)
        ret = []
        for source in sorted(sources):
            t = [source]
            for target in sorted(sources):
                try:
                    t.append(round(np.median(d[source][target][measure]), 2))
                except:
                    t.append('X')
            writer.writerow(t)
            # removing X
            t.remove('X')
            print t
            ret.append([source, np.median(t[1:])])
        myFile.close()
print 'Done!'