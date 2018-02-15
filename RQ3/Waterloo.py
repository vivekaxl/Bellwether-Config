from __future__ import division, print_function

import os
import pandas as pd
from pdb import set_trace
from metrics import rank_diff
from DataUtil import get_all_projects
from Model import train_prediction_model, train_transfer_model


def main()
    data_path = os.path.realpath("./data")
    projects = get_all_projects(data_path)

    for project in projects:
        files = project.files()
        for source_name, source_conf in files.iteritems():
            for target_name, target_conf in files.iteritems():

                if not source_name == target_name:

                    "Construct a prediction model using source"
                    predict_model = train_prediction_model(source_conf, T=5)

                    """Sample 15 from train and test datasets
                       to train a transfer model
                    """

                    "Find common configs between source and target"
                    common = pd.merge(source_conf, target_conf, how="inner")

                    "Pick random 15 samples"
                    some = common.sample(n=15)

                    "Get the dependent variables to construct a LR model"
                    p_src = some[source_conf.columns[-1]]
                    p_tgt = some[target_conf.columns[-1]]

                    "Train a transfer model"
                    transfer_model = train_transfer_model(
                        p_src=p_src, p_tgt=p_tgt)

                    "Remove elements used to train transfer model from target"
                    target_conf.drop(some.index, inplace=True)

                    "Perform tansfer"
                    target_indep = target_conf[target_conf.columns[:-1]]
                    target_actual = target_conf[target_conf.columns[-1]]
                    predicted_raw = predict_model.predict(
                        target_indep).reshape(-1, 1)
                    target_predicted = transfer_model.predict(
                        predicted_raw).reshape(1, -1)[0]
                    
                    "Get rank difference"
                    r_diff = rank_diff(actual=target_actual,
                                       predicted=target_predicted)
    
    # -------------------- DEBUG -------------------- #
                    set_trace()


if __name__ == "__main__":
    main()
