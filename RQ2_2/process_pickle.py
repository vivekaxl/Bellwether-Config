import pickle
import os

folders = [d for d in os.listdir('.') if 'PickleLocker' in d]

for folder in folders:
    collector = {}
    pfiles = [f for f in os.listdir(folder) if '.p' in f]
    for pfile in pfiles:
        tname = pfile.replace('.p', '')
        source_name = tname.split('|')[0]
        target_name = tname.split('|')[1]
        measure = tname.split('|')[2]
        fraction = tname.split('|')[3]

        if source_name not in collector.keys(): collector[source_name] = {}
        if target_name not in collector[source_name].keys(): collector[source_name][target_name] = {}
        if fraction not in collector[source_name][target_name].keys(): collector[source_name][target_name][fraction] = {}

        collector[source_name][target_name][fraction] = {}
        collector[source_name][target_name][fraction]['bellwether'] = None
        collector[source_name][target_name][fraction]['target'] = None

        content = pickle.load(open(folder + '/' + pfile))
        assert (len(content.keys()) == 1), "Something is wrong"
        source_key = content.keys()[0]
        assert (len(content[source_key].keys()) == 1), "Something is wrong"
        target_key = content[source_key].keys()[0]
        assert (len(content[source_key][target_key].keys()) == 1), "Something is wrong"
        fraction_key = content[source_key][target_key].keys()[0]
        assert (len(content[source_key][target_key][fraction_key].keys()) == 1), "Something is wrong"

        measure_key = content[source_key][target_key][fraction_key].keys()[0]
        assert (len(content[source_key][target_key][fraction_key][measure_key].keys()) == 2), "Something is wrong"

        collector[source_name][target_name][fraction]['bellwether'] = content[source_key][target_key][fraction_key][measure_key]['bellwether']
        collector[source_name][target_name][fraction]['target'] = content[source_key][target_key][fraction_key][measure_key]['target']
    pickle.dump(collector, open('./Processed/' + folder.split('_')[1].replace('/', '') + '.p', 'w'))


print 'Done'