import pickle
import os
import numpy as np
import pandas as pd
from pylab import rcParams
rcParams['figure.figsize'] =  10,5

def find_no_of_configuration(filename):
    return pd.read_csv(filename).shape[0]

pickle_folder = './Processed/'
files = [pickle_folder+file for file in os.listdir(pickle_folder) if '.p' in file]
consolidated = {}
for file in files:
    consolidated[file] = {}
    measurements = {}

    print file
    system_name = file.split('/')[-1].split('.p')[0]
    dd = pickle.load(open(file))
    print dd.keys()
    bw_file = "../Data/" + dd.keys()[0] + ".csv"
    # no of configurations in bellwether

    assert(len(dd.keys()) == 1), "Something is wrong"
    source = dd.keys()[0]
    targets = dd[source].keys()
    print file, len(targets)

    temp = {}
    for target in targets:
        measurements[target] = find_no_of_configuration("../Data/" + target + ".csv")
        percs = sorted(dd[source][target].keys(), key=lambda x: int(x))
        if len(temp.keys()) == 0:
            for perc in percs: temp[perc] = []
        for perc in percs:
            bw = dd[source][target][perc]['bellwether']
            tar =  dd[source][target][perc]['target']
            temp[perc].append(tar)
            # print file, target, perc, np.median(tar), np.median(bw)

    print measurements
    for key in temp.keys():
        consolidated[file][key] = [np.median(temp[key]), sum([int(key)*0.01*measurements[target] for target in targets])]
        print file, key, np.median(temp[key]), sum([int(key)*0.01*measurements[target] for target in targets]), np.median(bw), measurements[targets[0]]
        consolidated[file]['bw'] = [np.median(bw), measurements[targets[0]]*0.1]

    x = []
    y = []
    markers = ["*", "x", "s", "+", ".", "o", "v", "^", 'p']
    keys = ['bw', '10', '20', '30', '40', '50', '60', '70', '80', '90', '100', ]

    import matplotlib.pyplot as plt
    name = file.split('/')[-1].replace('.p', '')
    # plt.title(name)
    for key in keys:
        x.append(consolidated[file][key][0])
        y.append(consolidated[file][key][1])
    keys = ['Ex', '10%', '20%', '30%', '40%', '50%', '60%', '70%', '80%', '90%', '100%', ]

    # for xx, yy, marker in zip(x[1:], y[1:], markers[1:]):
    plt.plot( y[1:],x[1:], 'v--', markersize=10, color='gray', label='Non-tranfer Learning')
    plt.scatter( y[0], x[0], marker='o', s=344, color='#F27781', label='BEETLE')
    plt.ylabel('NAR (%)', fontsize=16)
    plt.xlabel('Number of Measurements', fontsize=16)
    # plt.xscale('log')
    # plt.ylim(0, 11000)
    plt.legend(loc='upper center', bbox_to_anchor=(0.5, 1.10), ncol=2, fancybox=True, frameon=False)
    print keys[0], x[0] * 1.03, y[0]
    plt.annotate(keys[0], xy=(x[0] * 1.03, y[0]))
    for label, xx, yy in zip(keys[1:], x[1:], y[1:]):
        print label, xx, yy
        plt.annotate(label, xy=(yy*1.03, xx*1.05), fontsize=12)
    plt.tight_layout()
    plt.savefig("./Pareto/"+name)
    plt.cla()

print 'Done!'
