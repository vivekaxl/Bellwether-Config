import pickle
import os
import numpy as np
import csv
from sk import rdivDemo

pickle_folder = './Processed/'
files = [pickle_folder+file for file in os.listdir(pickle_folder) if '.p' in file]
result_folder = './Results/'
consolidated = {}
for file in files:
    print file
    system_name = file.split('/')[-1].split('.p')[0]
    dd = pickle.load(open(file))
    assert(len(dd.keys()) == 1), "Something is wrong"
    source = dd.keys()[0]
    targets = dd[source].keys()
    myFile = open(result_folder + system_name + '.csv', 'w')
    writer = csv.writer(myFile)
    heading = ['Target Files', '5', '10', '15', '20', '25', '30', '35', '40', 's5', 's10', 's15', 's20', 's25', 's30', 's35', 's40']
    writer.writerow(heading)

    for target in targets:
        percs = sorted(dd[source][target].keys(), key=lambda x: int(x))
        t = [target]
        aux = []
        for perc in percs:
            print perc
            bw = ['bw'] + dd[source][target][perc]['bellwether']
            tar = ['target'] + dd[source][target][perc]['target']
            ret = rdivDemo('a', [bw, tar], globalMinMax=False, isLatex=False)
            for r in ret:
                if ret[0][2].name == 'bw':
                    bw_sk_rank = ret[0][0]
                    target_sk_rank = ret[1][0]
                else:
                    bw_sk_rank = ret[1][0]
                    target_sk_rank = ret[0][0]

            t.append(np.median(tar[1:]) - np.median(bw[1:]))
            if bw_sk_rank < target_sk_rank:
                aux.append('better')
            elif bw_sk_rank == target_sk_rank:
                aux.append('same')
            else:
                aux.append('worse')

        writer.writerow(t+aux)
    myFile.close()
print 'Done!'
