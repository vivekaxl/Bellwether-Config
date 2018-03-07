from __future__ import print_function
import os
import csv
import numpy as np
from pdb import set_trace
from MiscUtils import Misc
import multiprocessing as mp
from sk import sk_ranks, rdivDemo
from DataUtil import get_all_projects
from TransferLearners import Pooyan, Baseline, Waterloo


class BestWorst(object):
    "Compare the difference between using the best and the worst datasets"
    @classmethod
    def compare(self, data_pairs):
        data_path = os.path.realpath("./data")
        projects = get_all_projects(data_path)
        for project in projects:
            print(project.name.upper())
            files = project.files()
            best, worst = data_pairs[project.name]
            rest = [dframe for fname, dframe in files.iteritems() if fname not in data_pairs[project.name]]
            best_results = ["best"]
            worst_results = ["worst"]
            for tgt in rest:
                best_results.extend([Pooyan.learner(files[best], tgt) for _ in xrange(1)])
                worst_results.extend([Pooyan.learner(files[worst], tgt) for _ in xrange(1)])
            
            rdivDemo([best_results, worst_results])

            set_trace()


if __name__ == "__main__":
    best_worst = BestWorst()
    best_worst.compare(data_pairs={
        'sac': ('sac_6', 'sac_5'),
        'spear': ('spear_7', 'spear_3'),
        'x264': ('x264_18', 'x264_0'),
        'sqlite': ('sqlite_17', 'sqlite_94'),
        'storm-obj2': ('storm-obj2_feature7', 'storm-obj2_feature9')
    })
    


