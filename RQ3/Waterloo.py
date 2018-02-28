from __future__ import division, print_function

import os
import numpy as np
import pandas as pd
from pdb import set_trace
from metrics import rank_diff, mag_abs_error
from DataUtil import get_all_projects
from Model import train_prediction_model, train_transfer_model

def waterloo(source_conf, target_conf):
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
    predict_model = train_prediction_model(source_conf)

    """Sample 15 from train and test datasets to train a transfer model"""

    "Find common configs between source and target"
    common = pd.merge(source_conf, target_conf, how="inner")

    "Pick random 5, 10, or 15 samples"
    some = common.sample(n=5)

    "Get the dependent variables to construct a LR model"
    p_src = some[source_conf.columns[-1]]
    p_tgt = some[target_conf.columns[-1]]

    "Train a transfer model"
    transfer_model = train_transfer_model(
        p_src=p_src, p_tgt=p_tgt)

    "Remove elements used to train transfer model from target"
    target_conf = target_conf.drop(
        some.index, errors="ignore")

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





def main(n_reps=30):
    data_path = os.path.realpath("./data")
    projects = get_all_projects(data_path)
    results = dict()
    for project in projects:
        files = project.files()
        results_0 = dict()
        for source_name, source_conf in files.iteritems():
            results_0.update({source_name: {}})
            for target_name, target_conf in files.iteritems():
                if not source_name == target_name:
                    r_diff = []
                    for _ in xrange(n_reps):
                        "Construct a prediction model using source"
                        predict_model = train_prediction_model(
                            source_conf, T=5)

                        """Sample 15 from train and test datasets
                        to train a transfer model
                        """

                        "Find common configs between source and target"
                        common = pd.merge(
                            source_conf, target_conf, how="inner")

                        "Pick random 15 samples"
                        some = common.sample(n=10)

                        "Get the dependent variables to construct a LR model"
                        p_src = some[source_conf.columns[-1]]
                        p_tgt = some[target_conf.columns[-1]]

                        "Train a transfer model"
                        transfer_model = train_transfer_model(
                            p_src=p_src, p_tgt=p_tgt)

                        "Remove elements used to train transfer model from target"
                        target_conf = target_conf.drop(
                            some.index, errors="ignore")

                        "Perform tansfer"
                        target_indep = target_conf[target_conf.columns[:-1]]
                        target_actual = target_conf[target_conf.columns[-1]]
                        predicted_raw = predict_model.predict(
                            target_indep).reshape(-1, 1)
                        target_predicted = transfer_model.predict(
                            predicted_raw).reshape(1, -1)[0]

                        "Get rank difference"
                        r_diff.append(rank_diff(actual=target_actual,
                                            predicted=target_predicted))

                    results_0[source_name].update(
                        {target_name: int(np.median(r_diff))})

        results.update({project.name: pd.DataFrame(results_0)})
    # -------------------- DEBUG -------------------- #
    set_trace()


if __name__ == "__main__":
    main(n_reps=31)
