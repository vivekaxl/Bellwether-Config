import numpy as np


def rank_diff(actual, predicted):
    actual_ranks = np.argsort(actual).tolist()[0]
    predicted_ranks = predicted[actual_ranks]
    diff = abs(actual_ranks - predicted_ranks)
    return diff
