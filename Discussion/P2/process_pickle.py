import os
import pickle
import numpy as np


folders = ['PickleLocker_sac/', 'PickleLocker_spear/', 'PickleLocker_sqlite/', 'PickleLocker_storm-obj1/', 'PickleLocker_storm-obj2/',
           'PickleLocker_x264/']

for folder in folders:
    all_content = {}
    files = [folder + f for f in os.listdir(folder) if '.p' in f]
    for file in files:
        t = file.split('/')[-1].replace('.p', '')
        source = t.split('|')[0]
        target = t.split('|')[1]
        percent = t.split('|')[2]

        content = pickle.load(open(file))
        assert(len(content.keys()) == 1), "Something is wrong"
        key1 = content.keys()[-1]
        key2 = content[key1].keys()[-1]
        key3 =content[key1][key2].keys()[-1]
        print key1, key2
        if key1 not in all_content.keys():
            all_content[key1] = {}
        if key2 not in all_content[key1].keys():
            all_content[key1][key2] = {}

        all_content[key1][key2][key3] = content[key1][key2][key3]
    pickle_file = './PickleLocker/' + folder[:-1] + "_1-16.p"
    pickle.dump(all_content, open(pickle_file, 'w'))
