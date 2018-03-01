import scipy as sp
import numpy as np
from pdb import set_trace
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.gaussian_process import GaussianProcessRegressor
from kernel import SEAMS_Kernel

class Model:

    @classmethod
    def train_prediction_model(cls, data_source, T=5):
        """
        Train a prediction model using Regression Tree

        :param data_source: A pandas dataframe of the source dataset
        :type  data_source: Pandas DataFrame
        :param T: Training coefficient
        :type  T: int
        :return: Decision Tree Model
        """

        clf = DecisionTreeRegressor()
        N_f = len(data_source.columns)
        n_samples = T * N_f
        sampled = data_source.sample(n=n_samples)
        indep_vars = sampled[sampled.columns[:-1]]
        depend_var = sampled[sampled.columns[-1]]
        return clf.fit(X=indep_vars, y=depend_var)

    @classmethod
    def train_transfer_model(cls, p_src, p_tgt):
        """
        Train a transfer model to transfer predictions to target from source

        :param p_src: performance value of configs C on source
        :type  p_src: list
        :param p_tgt: performance value of configs C on target
        :type  p_tgt: list
        :return: Linear Regression Model
        """

        clf = LinearRegression()
        return clf.fit(X=p_src.reshape(-1, 1), y=p_tgt.reshape(-1, 1))

    @classmethod
    def train_gaussproc_model(cls, src_config, tgt_config):
        """
        Train a Gaussian processes model to transfer 
        predictions to target from source

        :param src_config: Source configurations
        :type  src_config: pandas.core.frame.DataFrame
        :param tgt_config: Target configurations
        :type  tgt_config: pandas.core.frame.DataFrame
        :rtype: sklearn gaussian processes model
        """
        
        src_indep_vars = src_config[src_config.columns[:-1]]
        src_depend_var = src_config[src_config.columns[-1]]
        tgt_depend_var = tgt_config[tgt_config.columns[-1]]
        corr = np.mean(np.correlate(src_depend_var, tgt_depend_var))
        kernel = SEAMS_Kernel(corr) 
        clf = GaussianProcessRegressor(kernel=kernel)
        return clf.fit(X=src_indep_vars, y=src_depend_var)

    @classmethod
    def train_baseline_model(cls, src_config):
        """
        Train a Gaussian processes model to transfer 
        predictions to target from source

        :param src_config: Source configurations
        :type  src_config: pandas.core.frame.DataFrame
        :param tgt_config: Target configurations
        :type  tgt_config: pandas.core.frame.DataFrame
        :rtype: sklearn decisiontree model
        """

        src_indep_vars = src_config[src_config.columns[:-1]]
        src_depend_var = src_config[src_config.columns[-1]]
        clf = DecisionTreeRegressor()
        return clf.fit(src_indep_vars, src_depend_var)
