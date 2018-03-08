import numpy as np
content = open('data2.csv').readlines()

consolidated = {}
for c in content:
    step_size, lives, value = map(float, c.strip().split(','))
    if step_size not in consolidated.keys():
        consolidated[step_size] = {}
    if lives not in consolidated[step_size].keys():
        consolidated[step_size][lives] = [float(value)]
    else:
        print consolidated
        print step_size, lives
        consolidated[step_size][lives].append(value)

for step_size in sorted(consolidated.keys()):
    for live in sorted(consolidated[step_size].keys()):
        print step_size, live, np.median(consolidated[step_size][live])
import pdb
pdb.set_trace()