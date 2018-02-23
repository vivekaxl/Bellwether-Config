import pickle
import os

folders = [  'PickleLocker_sqlite/', 'PickleLocker_x264/', 'PickleLocker_spear/', 'PickleLocker_sac/','./PickleLocker_storm-obj1/', './PickleLocker_storm-obj2/']


for folder in folders:
    collector = {}
    pfiles = [f for f in os.listdir(folder) if '.p' in f]
    for pfile in pfiles:
        tname = pfile.replace('.p', '')
        source_name = tname.split('|')[0]
        target_name = tname.split('|')[1]
        measure = tname.split('|')[2]

        if source_name not in collector.keys(): collector[source_name] = {}
        if target_name not in collector[source_name].keys(): collector[source_name][target_name] = {}
        if measure not in collector[source_name][target_name].keys(): collector[source_name][target_name][measure] = None

        content = pickle.load(open(folder + pfile))
        assert(len(content.keys()) == 1), "Something is wrong"
        source_key = content.keys()[0]
        assert (len(content[source_key].keys()) == 1), "Something is wrong"
        target_key = content[source_key].keys()[0]
        assert(len(content[source_key][target_key].keys()) == 1), "Something is wrong"
        measure_key = content[source_key][target_key].keys()[0]


        collector[source_name][target_name][measure] = content[source_key][target_key][measure_key]

    pickle.dump(collector, open('./Processed/' + folder.split('_')[1].replace('/','') + '.p', 'w'))


