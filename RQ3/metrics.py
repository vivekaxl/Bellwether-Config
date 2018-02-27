import numpy as np
from pdb import set_trace

def rank_diff(actual, predicted):
    actual_ranks = np.argsort(actual).tolist()[0]
    predicted_val = predicted[actual_ranks]
    predicted_ranks = [i for i, val in enumerate(predicted) if val == predicted_val]
    diff = abs(actual_ranks - predicted_ranks[-1])
    return diff
