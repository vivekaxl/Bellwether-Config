from __future__ import division, print_function

import os
import numpy as np
import pandas as pd
from pdb import set_trace
from metrics import rank_diff
from DataUtil import get_all_projects
from Model import train_gaussproc_model

def pooyan(source_conf, target_conf):
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
    predict_model = train_gaussproc_model(
        source_conf, target_conf)

    "Perform tansfer"
    target_indep = target_conf[target_conf.columns[:-1]]
    target_actual = target_conf[target_conf.columns[-1]]
    target_predicted = predict_model.predict(
        target_indep).reshape(-1, 1)

    "Get MMRE"
    mmre = np.mean(abs(target_actual - target_predicted))
    return mmre


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

                        "Get the dependent variables to construct a LR model"
                        p_src = source_conf[source_conf.columns[-1]]
                        p_tgt = target_conf[target_conf.columns[-1]]

                        "Construct a gaussian process model using source"
                        predict_model = train_gaussproc_model(
                            source_conf, target_conf)

                        "Perform tansfer"
                        target_indep = target_conf[target_conf.columns[:-1]]
                        target_actual = target_conf[target_conf.columns[-1]]
                        target_predicted = predict_model.predict(
                            target_indep).reshape(-1, 1)
                        

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
