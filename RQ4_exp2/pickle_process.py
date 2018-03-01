import pickle
import numpy as np


pickle_file = "./experiment_pickle.p"

content = pickle.load(open(pickle_file))

familys = content.keys()

for family in familys:

    reps = content[family]
    assert(len(reps) == 20), "Something is wrong"
    print family, np.median([np.median(rep[1]) for rep in reps])
    if family == 'spear':
        import pdb
        pdb.set_trace()
import pdb
pdb.set_trace()