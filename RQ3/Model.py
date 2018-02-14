from sklearn.tree import DecisionTreeRegressor

def train_prediction_model(data_source, test, T=5):
    """
    Train a prediction model using Regression Tree

    :param data_source: A pandas dataframe of the source dataset
    :type data_source: Pandas DataFrame
    :param T: Training coefficient
    :type T: int
    :return: Model
    """

    clf = DecisionTreeRegressor()
    N_f = len(data_source.columns)
    n_samples = T * N_f
    sampled = data_source.sample(n=n_samples)
    indep_vars = sampled[sampled.columns[:-1]]
    depend_var = sampled[sampled.columns[-1]]
    return clf.fit(X=indep_vars, y=depend_var)
