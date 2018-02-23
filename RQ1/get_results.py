import pickle
import os
import numpy as np
import csv

pickle_folder = './Processed/'
measures = ['rank', 'mmre', 'abs_res']
files = [pickle_folder+file for file in os.listdir(pickle_folder) if '.p' in file]
result_folder = './Results/'
for file in files:
    system_name = file.split('/')[-1].split('.p')[0]
    for measure in measures:
        myFile = open(result_folder + system_name + '_' + measure + '.csv', 'w')
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
            ret.append([source, np.median(t[1:])])
        print [x[0] for x in sorted(ret, key=lambda x:x[1])][:3]
        myFile.close()
print 'Done!'