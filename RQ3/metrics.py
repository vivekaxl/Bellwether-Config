import numpy as np
from pdb import set_trace

def rank_diff(actual, predicted):
    predicted_rank = np.argsort(predicted).tolist()[0]
    actual_val = actual.values[predicted_rank]
    diff = [i for i, val in enumerate(sorted(actual.values)) if val == actual_val] 
    return diff[0]

def mag_abs_error(actual, predicted):
    predicted_rank = np.argsort(predicted).tolist()[0]
    actual_val = actual.values[predicted_rank]
    diff = abs(min(actual) - actual_val) * 100
    return diff

def _test0():
    actual = [1, 2, 0, 5]
    predic = [3, 7, 2, 8]
    print rank_diff(actual, predic)
    assert rank_diff(actual, predic) == 0


def _test1():
    actual = [5, 2, 1, 3]
    predic = [1, 2, 3, 5]
    print mag_abs_error(actual, predic)
    assert mag_abs_error(actual, predic) == 400


if __name__ == "__main__":
    _test1()
