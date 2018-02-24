from __future__ import division
import pandas as pd
import pickle
import os
from os import listdir
from random import randint, shuffle
from sklearn.tree import DecisionTreeRegressor


class solution_holder:
    def __init__(self, id, decisions, objective, rank):
        self.id = id
        self.decision = decisions
        self.objective = objective
        self.rank = rank


def get_data(filename, seeds):
    """
    :param filename:
    :param Initial training size
    :return: Training and Testing
    """
    pdcontent = pd.read_csv(filename)
    indepcolumns = [col for col in pdcontent.columns if "<$" not in col]
    depcolumns = [col for col in pdcontent.columns if "<$" in col]
    sortedpdcontent = pdcontent.sort(depcolumns[-1])
    # Since several independent values have the same depedent value
    ranks = {}
    for i, item in enumerate(sorted(set(sortedpdcontent[depcolumns[-1]].tolist()))): ranks[item] = i

    # For fast lookup. Better way would be to use pandas
    data = {}
    for id in xrange(pdcontent.shape[0]):
        item = pdcontent.iloc[id]
        indep = ','.join(map(str, map(int, item[indepcolumns].tolist())))
        data[indep] = id
    # assert(len(data.keys()) == pdcontent.shape[0]), "Something is wrong" -> removed due to existing duplicates

    # find indexes of entries which have seeds as independent variable
    train_indexes = []
    for id in xrange(seeds.shape[0]):
        item = seeds.iloc[id]
        indep = ','.join(map(str, map(int, item[indepcolumns].tolist())))
        try:
            train_indexes.append(data[indep])
        except: pass

    # Sometimes when all the seeds (from BW dataset) are not found in the target dataset
    if len(train_indexes) < seeds.shape[0]:
        print 'seeds not found: ', filename, seeds.shape[0] - len(train_indexes)
        # add random seeds
        indexes = range(pdcontent.shape[0])
        # remove all the indexes already in seed
        for train_index in sorted(train_indexes, reverse=True):
            del indexes[train_index]
        assert(len(indexes) + seeds.shape[0] ==  pdcontent.shape[0]), "Something is wrong"

        # filling up train indexes
        while len(train_indexes) != seeds.shape[0]:
            # get a random index
            random_index = randint(0, len(indexes))
            train_indexes.append(random_index)
            del indexes[random_index]

    # Getting test indexes by removing the train_indexes
    test_indexes = range(pdcontent.shape[0])
    for train_index in sorted(train_indexes, reverse=True): del test_indexes[train_index]
    shuffle(test_indexes)
    assert(len(train_indexes) + len(test_indexes) == pdcontent.shape[0]), "Somethign is wrong"

    content = list()
    for c in xrange(len(sortedpdcontent)):
        content.append(solution_holder(
            c,
            sortedpdcontent.iloc[c][indepcolumns].tolist(),
            sortedpdcontent.iloc[c][depcolumns].tolist(),
            ranks[sortedpdcontent.iloc[c][depcolumns].tolist()[-1]]
        )
        )

    train_set = [content[i] for i in train_indexes]
    test_set = [content[i] for i in test_indexes]

    assert(len(train_set) + len(test_set) == pdcontent.shape[0]), "Somethign is wrong"
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


def run_active_learning(filename, seeds, max_lives=10, budget=30):
    steps = 0
    training_set, testing_set = get_data(filename, seeds)
    dataset_size = len(training_set) + len(testing_set)
    while (initial_size+steps) < dataset_size - 1:
        best_id = get_best_configuration_id(training_set, testing_set)
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


def get_top_performing(filename, initial_size):
    """Get top performing candidates from the filename"""
    pdcontent = pd.read_csv(filename)
    indepcolumns = [col for col in pdcontent.columns if "<$" not in col]
    depcolumns = [col for col in pdcontent.columns if "<$" in col]
    sortpdcontent = pdcontent.sort(depcolumns[-1])

    seeds_all = sortpdcontent[:initial_size]
    seeds = seeds_all[indepcolumns]
    assert(seeds.shape[0] == initial_size), "Somethign is wrong"
    return seeds


def wrapper_run_active_learning(filename, seeds, rep, budget):

    print filename, initial_size, rep, budget
    training_set, testing_set= run_active_learning(filename, seeds, budget)
    directory_name = './BWLocker/' + filename.replace('../../Data/', '').replace('.csv', '').split('_')[0] + '/'
    if not os.path.exists(directory_name):
        os.makedirs(directory_name)
    pickle_file = directory_name + filename.replace('../../Data/', '').replace('.csv', '') + '|' + str(rep) + '|' + str(budget) + '.p'
    pickle.dump([t.rank for t in training_set], open(pickle_file, 'w'))

if __name__ == "__main__":
    bellwethers = {
        'sac': 'sac_5',
        'spear': 'spear_7',
        'x264': 'x264_9',
        'sqlite': 'sqlite_19'
    }
    seeds_dict = {}
    initial_size = 20
    for family in bellwethers.keys():
        # get top performing candidates from the bellwether data
        bellwether_file = '../../Data/' + bellwethers[family] + '.csv'
        seeds_dict[family] = get_top_performing(bellwether_file, initial_size)
    import multiprocessing as mp
    # Main control loop
    pool = mp.Pool()

    data_folder = "../../Data/"
    filenames = [data_folder+f for f in listdir(data_folder) if '.csv' in f]
    initial_size = 10
    budgets = [ 30, 40, 50, 60]
    evals_dict = {}
    rank_diffs_dict = {}
    stats_dict = {}
    for filename in filenames:
        for budget in budgets:
            for rep in xrange(20):
                family = filename.replace('../../Data/', '').replace('.csv', '').split('_')[0]
                system = filename.replace('../../Data/', '').replace('.csv', '')
                if bellwethers[family] == system:
                    # if bellwether then exit
                    continue
                else:
                    # pool.apply_async(wrapper_run_active_learning, (filename, seeds_dict[family], rep, budget))
                    # print filename, rep, budget
                    wrapper_run_active_learning(filename, seeds_dict[family], rep, budget)
    pool.close()
    pool.join()


