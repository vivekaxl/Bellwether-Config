from __future__ import division
import pandas as pd
import pickle
import os
from os import listdir
from random import shuffle
from sklearn.tree import DecisionTreeRegressor


class solution_holder:
    def __init__(self, id, decisions, objective, rank):
        self.id = id
        self.decision = decisions
        self.objective = objective
        self.rank = rank


def get_data(filename, initial_size):
    """
    :param filename:
    :param Initial training size
    :return: Training and Testing
    """
    pdcontent = pd.read_csv(filename)
    indepcolumns = [col for col in pdcontent.columns if "<$" not in col]
    depcolumns = [col for col in pdcontent.columns if "<$" in col]
    sortpdcontent = pdcontent.sort(depcolumns[-1])
    ranks = {}
    for i, item in enumerate(sorted(set(sortpdcontent[depcolumns[-1]].tolist()))):
        ranks[item] = i

    content = list()
    for c in xrange(len(sortpdcontent)):
        content.append(solution_holder(
                                       c,
                                       sortpdcontent.iloc[c][indepcolumns].tolist(),
                                       sortpdcontent.iloc[c][depcolumns].tolist(),
                                       ranks[sortpdcontent.iloc[c][depcolumns].tolist()[-1]]
                                       )
                       )

    shuffle(content)
    indexes = range(len(content))
    train_indexes, test_indexes = indexes[:initial_size],  indexes[initial_size:]
    assert(len(train_indexes) + len(test_indexes) == len(indexes)), "Something is wrong"
    train_set = [content[i] for i in train_indexes]
    test_set = [content[i] for i in test_indexes]

    return [train_set, test_set]


def get_best_configuration_id(train, test):
    train_independent = [t.decision for t in train]
    train_dependent = [t.objective[-1] for t in train]

    test_independent = [t.decision for t in test]

    model = DecisionTreeRegressor()
    model.fit(train_independent, train_dependent)
    predicted = model.predict(test_independent)
    predicted_id = [[t.id,p] for t,p in zip(test, predicted)]
    predicted_sorted = sorted(predicted_id, key=lambda x: x[-1])
    # Find index of the best predicted configuration
    best_index = predicted_sorted[0][0]
    return best_index


def run_active_learning(filename, initial_size, max_lives=10, budget=30):
    steps = 0
    lives = max_lives
    training_set, testing_set = get_data(filename, initial_size)
    dataset_size = len(training_set) + len(testing_set)
    while (initial_size+steps) < dataset_size - 1:
        best_id = get_best_configuration_id(training_set, testing_set)
        # print best_index, len(testing_set)
        best_solution = [t for t in testing_set if t.id == best_id][-1]
        training_set.append(best_solution)
        # find index of the best_index
        best_index = [i for i in xrange(len(testing_set)) if testing_set[i].id == best_id]
        assert(len(best_index) == 1), "Something is wrong"
        best_index = best_index[-1]
        del testing_set[best_index]
        assert(len(training_set) + len(testing_set) == dataset_size), "Something is wrong"
        if len(training_set) >= budget:
            break
        steps += 1

    return training_set, testing_set


def wrapper_run_active_learning(filename, initial_size, rep, budget):
    print filename, initial_size, rep, budget
    training_set, testing_set= run_active_learning(filename, initial_size, budget)
    global_min = min([t.objective[-1] for t in training_set + testing_set])
    best_training_solution = [ tt.rank for tt in training_set if min([t.objective[-1] for t in training_set]) == tt.objective[-1]]
    best_solution = [tt.rank for tt in training_set + testing_set if tt.objective[-1] == global_min]
    directory_name = './FlashLocker/' + filename.replace('../../Data/', '').replace('.csv', '').split('_')[0] + '/'
    if not os.path.exists(directory_name):
        os.makedirs(directory_name)
    pickle_file = directory_name + filename.replace('../../Data/', '').replace('.csv', '') + '|' + str(rep) + '|' + str(budget) + '.p'
    pickle.dump([t.rank for t in training_set], open(pickle_file, 'w'))

if __name__ == "__main__":
    import multiprocessing as mp
    # Main control loop
    pool = mp.Pool()

    data_folder = "../../Data/"
    filenames = [data_folder+f for f in listdir(data_folder) if '.csv' in f and 'sqlite' not in f]
    initial_size = 10
    budgets = [ 30, 40, 50, 60]
    evals_dict = {}
    rank_diffs_dict = {}
    stats_dict = {}
    for filename in filenames:
        for budget in budgets:
            for rep in xrange(20):
                pool.apply_async(wrapper_run_active_learning, (filename, initial_size, rep, budget))
                # wrapper_run_active_learning(filename, initial_size, rep, budget)
    pool.close()
    pool.join()


