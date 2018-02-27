import pickle
import numpy as np

pickle_file = 'experiment_pickle_4_0.1_4.p'

content = pickle.load(open(pickle_file))

familys = content.keys()

for family in familys:
    collected = []
    measurements = content[family]
    for measurement in measurements:
        collected.append(np.mean(measurement[1]))
    print family, [round(c, 3) for c in collected], np.median(collected)
