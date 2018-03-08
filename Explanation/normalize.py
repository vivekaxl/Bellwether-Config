import pandas as pd
import os

data_folder = "../allData/"
files = [data_folder + f for f in os.listdir(data_folder) if ".csv" in f]
files = [f for f in files if 'sac' in f]

for f in files:
    train_content = pd.read_csv(f)
    train_cols = train_content.columns.values.tolist()
    ctrain_indep = [c for c in train_cols if '<$' not in c]
    ctrain_dep = [c for c in train_cols if '<$' in c]
    assert (len(ctrain_dep) == 1), "Something is wrong"

    ctrain_dep = ctrain_dep[0]

    train_content2 = train_content
    train_content2[ctrain_dep] = (train_content[ctrain_dep] - train_content[ctrain_dep].min())/(train_content[ctrain_dep].max() - train_content[ctrain_dep].min())

    name = f.split('/')[-1]

    train_content2.to_csv('./Normal/' + name, index = False)
print "Done"