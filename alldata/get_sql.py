from __future__ import division
import os
import pandas as pd
import numpy as np


files = [f for f in os.listdir('.') if '.csv' in f and 'sql' in f]
n_files = [f for f in os.listdir('.') if '.csv' in f and 'sql' not in f]

for n_file in n_files:
    os.system('cp ' + n_file + ' ' + '../Data/'+n_file)

t = []
for file in files:
    content = pd.read_csv(file)
    columns = content.columns
    indep = [c for c in columns if '<$' not in c]
    dep = [c for c in columns if '<$' in c]
    assert(len(dep) == 1), "Something is wrong"

    d_c = [c[-1] for c in content[dep].values.tolist()]  # Since c is a list of length 1
    t.append([file, max(d_c)-min(d_c)])

for tt in sorted(t, key=lambda x:x[1], reverse=True)[:15]:
    os.system('cp ' + tt[0] + ' ' + '../Data/' + tt[0])




