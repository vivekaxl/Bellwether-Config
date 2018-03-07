from __future__ import print_function
import os
import csv
import numpy as np
from pdb import set_trace
from MiscUtils import Misc
import multiprocessing as mp
from sk import rdivDemo
from DataUtil import get_all_projects
from TransferLearners import Pooyan, Baseline, Waterloo

class ResearchQuestion4:
    def get_reults(self, bellwethers=None, n_reps=12):
        data_path = os.path.realpath("./data")
        projects = get_all_projects(data_path)
        for project in projects:
            print(project.name.upper())
            files = project.files()
            results_0 = []
            for transfer in [Pooyan, Baseline, Waterloo]: 
                results_1 = [transfer.__doc__.upper()]
                for source_name, source_conf in files.iteritems():
                    for target_name, target_conf in files.iteritems():
                            if not source_name == target_name:
                                if transfer.__doc__ == "baseline": 
                                    if source_name in bellwethers[project.name]:
                                        results_1.extend([transfer.learner(source_conf, target_conf)
                                    for _ in xrange(n_reps)])
                                else:
                                    results_1.extend([transfer.learner(source_conf, target_conf)
                                                      for _ in xrange(n_reps)])
                results_0.append(results_1)
            rdivDemo(results_0)
            print("")

if __name__ == "__main__":
    rq4 = ResearchQuestion4()
    rq4.get_reults(bellwethers={
        'sac': ['sac_6'],
        'sqlite': ['sqlite_17'],
        'spear': ['spear_7', 'spear_1', 'spear_9'],
        'x264': ['x264_9', 'x264_10', 'x264_7', 'x264_1', 'x264_11', 'x264_8', 'x264_18', 'x264_6'],
        'storm-obj1': ['storm-obj1_feature8'],
        'storm-obj2': ['storm-obj2_feature9']}
    )
