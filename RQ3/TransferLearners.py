from __future__ import division, print_function

import os
import numpy as np
import pandas as pd
from pdb import set_trace
from DataUtil import get_all_projects
from metrics import rank_diff, mag_abs_error
from DataUtil import get_all_projects
from Models import Model


class Waterloo:
    "waterloo"
    @classmethod
    def learner(cls, source_conf, target_conf):
        """
        Run Waterloo's transfer learner

        :param source_conf: source dataset
        :type source_conf: str or pd.core.frame.DataFrame
        :param target_conf: target dataset
        :type target_conf: str or pd.core.frame.DataFrame
        :rtype: Float
        """
        source_conf = pd.read_csv(source_conf) if isinstance(
            source_conf, str) else source_conf

        target_conf = pd.read_csv(target_conf) if isinstance(
            target_conf, str) else target_conf

        "Construct a prediction model using source"
        predict_model = Model.train_prediction_model(source_conf)

        """Sample 15 from train and test datasets to train a transfer model"""


        "Pick random 5, 10, or 15 samples"
            
        "Common rows"
        if len(source_conf) <= len(target_conf):
            p_src = source_conf[source_conf.columns[-1]].sample(15)
            p_tgt = target_conf[target_conf.columns[-1]].iloc[p_src.index]
        else:
            p_tgt = target_conf[target_conf.columns[-1]].sample(15)
            p_src = source_conf[source_conf.columns[-1]].iloc[p_tgt.index]

        
        "Train a transfer model"
        transfer_model = Model.train_transfer_model(
            p_src=p_src, p_tgt=p_tgt)

        "Remove elements used to train transfer model from target"
        target_conf = target_conf.drop(
            p_tgt.index, errors="ignore")


        "Perform tansfer"
        target_indep = target_conf[target_conf.columns[:-1]]
        target_actual = target_conf[target_conf.columns[-1]]
        predicted_raw = predict_model.predict(
            target_indep).reshape(-1, 1)
        target_predicted = transfer_model.predict(
            predicted_raw).reshape(1, -1)[0]

        # "Get MMRE"
        # mmre = np.mean(abs(target_actual - target_predicted))
        # return mmre

        # "Get rank difference"
        # r_diff = rank_diff(actual=target_actual, predicted=target_predicted)
        # return r_diff

        "Get Magnitude of Error"
        me = mag_abs_error(actual=target_actual, predicted=target_predicted)
        return me


class Baseline:
    "baseline"
    @classmethod
    def learner(cls, source_conf, target_conf):
        """
        Run a baseline transfer learner

        :param source_conf: source dataset
        :type source_conf: str or pd.core.frame.DataFrame
        :param target_conf: target dataset
        :type target_conf: str or pd.core.frame.DataFrame
        :rtype: Float
        """

        source_conf = pd.read_csv(source_conf) if isinstance(
            source_conf, str) else source_conf

        target_conf = pd.read_csv(target_conf) if isinstance(
            target_conf, str) else target_conf

        "Construct a prediction model using source"
        predict_model = Model.train_baseline_model(source_conf)

        "Common rows"
    
        if len(source_conf) <= len(target_conf):
            p_src = source_conf[source_conf.columns[-1]]
            p_tgt = target_conf[target_conf.columns[-1]].iloc[p_src.index]
        else:
            p_tgt = target_conf[target_conf.columns[-1]]
            p_src = source_conf[source_conf.columns[-1]].iloc[p_tgt.index]

        "Train a transfer model"
        try: transfer_model = Model.train_transfer_model(p_src=p_src, p_tgt=p_tgt)
        except: set_trace()

        "Perform tansfer"
        target_indep = target_conf[target_conf.columns[:-1]]
        target_actual = target_conf[target_conf.columns[-1]]
        predicted_raw = predict_model.predict(
            target_indep).reshape(-1, 1)
        target_predicted = transfer_model.predict(
            predicted_raw).reshape(1, -1)[0]


        # "Get MMRE"
        # mmre = np.mean(abs(target_actual - target_predicted))
        # return mmre

        # "Get rank difference"
        # r_diff = rank_diff(actual=target_actual, predicted=target_predicted)
        # return r_diff

        "Get Magnitude of Error"
        me = mag_abs_error(actual=target_actual, predicted=target_predicted)
        return me

class Pooyan:
    "pooyan"
    @classmethod
    def learner(cls, source_conf, target_conf):
        """
        Run Pooyan's SEAMS transfer learner

        :param source_conf: source dataset
        :type source_conf: str or pd.core.frame.DataFrame
        :param target_conf: target dataset
        :type target_conf: str or pd.core.frame.DataFrame
        :rtype: Float
        """

        source_conf = pd.read_csv(source_conf) if isinstance(
            source_conf, str) else source_conf

        target_conf = pd.read_csv(target_conf) if isinstance(
            target_conf, str) else target_conf

        "Construct a gaussian process model using source"
        predict_model = Model.train_gaussproc_model(
            source_conf, target_conf)

        "Perform tansfer"
        target_indep = target_conf[target_conf.columns[:-1]]
        target_actual = target_conf[target_conf.columns[-1]]
        target_predicted = predict_model.predict(
            target_indep).reshape(-1, 1)

        "Perform tansfer"
        target_indep = target_conf[target_conf.columns[:-1]]
        target_actual = target_conf[target_conf.columns[-1]]
        target_predicted = predict_model.predict(
            target_indep).reshape(-1, 1)

        # "Get MMRE"
        # mmre = np.mean(abs(target_actual - target_predicted))
        # return mmre

        # "Get rank difference"
        # r_diff = rank_diff(actual=target_actual, predicted=target_predicted)
        # return r_diff

        "Get Magnitude of Error"
        me = mag_abs_error(actual=target_actual, predicted=target_predicted)
        return me



if __name__ == "__main__":
    main(n_reps=31)
