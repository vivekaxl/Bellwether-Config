from __future__ import division, print_function

import os
from pdb import set_trace
from DataUtil import get_all_projects

if __name__ == "__main__":

    data_path = os.path.realpath("../Data")
    for project in get_all_projects():
        set_trace()
