import pandas as pd
import pickle
import numpy as np
from sk import rdivDemo

file = "./Processed/processed_100.p"

content = pickle.load(open(file))


temp = content['x264'][100]

files = temp.keys()

ll = []
for source in files:
    targets = temp[source].keys()
    l = [source]
    for target in targets:
        l.append(np.median(temp[source][target]))
    ll.append(l)


rdivDemo('x264', ll, isLatex=False, globalMinMax=True,)

