import pickle
import os
import numpy as np
import csv
from glob2 import glob
from pdb import set_trace
from sk import rdivDemo

def sk_charts():
    pass

def main():
    files = glob("./Processed/*.p")
    for file in files:
        system_name = file.split('/')[-1].split('.p')[0]
        d = pickle.load(open(file))
        outer = []
        for src,val in d.iteritems():
            inner = [src]
            for _,v in val.iteritems():
                inner.extend(v['rank'])
            outer.append(inner)
        rdivDemo(outer)

if __name__ == "__main__":
    main()