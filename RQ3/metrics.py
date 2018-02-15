import numpy as np 

def rank_diff(actual, predicted):
    actual_ranks = np.argsort(actual)
    predicted_ranks = np.argsort(predicted)
    diff = abs(actual_ranks-predicted_ranks)
    return diff 
