from __future__ import print_function, division
import os
import pandas as pd
from abc import abstractmethod, ABCMeta
from glob2 import glob


class __ProjectBase(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def set_src(self, src):
        pass

    @abstractmethod
    def get_src(self):
        pass

    @abstractmethod
    def files(self):
        pass


class __Project(__ProjectBase):

    def __init__(self, name, src):
        self.name = name
        self.set_src(src)

    def set_src(self, src):
        self.src = src

    def get_src(self):
        return self.src

    def files(self):
        raw_paths = glob(os.path.join(self.src, "*.csv"))
        datasets = dict()
        for path in raw_paths:
            datasets.update({os.path.basename(path).rstrip(".csv"): pd.read_csv(path)})
        return datasets


def get_all_projects(data_path):
    """
    Returns all the projects in a path

    :param data_path: Path of data directories. Eg: data_path/1/, data_path/2,...
    :type data_path: str
    :return: A list of all the projects
    """

    all = []
    assert os.path.exists(data_path), "Invalid data path."
    for projects in glob(os.path.join(data_path, "*")):
        name = os.path.basename(projects)
        all += [__Project(name, src=projects)]

    return all
