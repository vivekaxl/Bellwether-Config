import pickle
import csv

pickle_file = 'feature_imp.p'

content = pickle.load(open(pickle_file))

familys = content.keys()

for family in familys:
    myfile = open('./Results_10-100/' + family + '.csv', 'w')
    writer = csv.writer(myfile)

    files = sorted(content[family].keys())
    for file in files:
        t = [file]
        source = file
        for target in files:
            if source == target:
                t.append(-1)
                continue
            source_features = content[family][source]
            target_features = content[family][target]

            count = 0
            for source_f in source_features:
                if source_f in target_features: count += 1
            # for s, tar in zip(source_features, target_features):
            #     if s == tar: count += 1

            print source_features, target_features, count
            t.append(count)
        writer.writerow(t)
    myfile.close()