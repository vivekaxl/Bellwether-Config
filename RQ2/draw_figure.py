from __future__ import division
import pickle
import os
import pandas as pd
import numpy as np
import matplotlib as mpl


# def draw(pickle_file, measure):
#     import matplotlib.pyplot as plt
#     name = pickle_file.split('/')[-1].replace('.p', '')
#     content = pickle.load(open(pickle_file))
#     sources = sorted(content.keys())
#
#     max_num = sys.maxint * -1
#     heatmap_arr = []
#     for source in sources:
#         t = []
#         for target in sources:
#
#             try:
#                 t.append(np.median(content[source][target][measure]))
#                 max_num = max(max_num, t[-1])
#             except:
#                 t.append(1000000)
#         heatmap_arr.append(t)
#
#     # # remove outliers
#     # for i, h in enumerate(heatmap_arr):
#     #     m = sum([hhh for hhh in h if 2000 != hhh]) / (len(h) - 1)
#     #     for j, hh in enumerate(h):
#     #         if hh > 4000:
#     #             heatmap_arr[i][j] = 8000
#
#     # imgplot = plt.imshow(heatmap_arr, cmap='seismic', interpolation='nearest')
#     # plt.xticks(range(len(sources)), sources, fontsize=12, rotation=90)
#     # plt.yticks(range(len(sources)), sources, fontsize=12)
#     # plt.colorbar(imgplot)
#     # plt.show()
#
#     fig, ax = plt.subplots()
#     # Using matshow here just because it sets the ticks up nicely. imshow is faster.
#     imgplot = ax.matshow(heatmap_arr, cmap='Greys', vmax=max_num)
#
#     for i in xrange(len(heatmap_arr)):
#         ax.add_patch(mpl.patches.Rectangle((i - .5, i - .5), 1, 1, hatch='X', fill=False, snap=False, color='white'))
#
#     # for (i, j), z in np.ndenumerate(heatmap_arr):
#     #     if z == 4000:
#     #         # ax.text(j, i, 'X', ha='center', va='center', color='black')
#     #         pass
#     #     else:
#     #         ax.text(j, i, '{:0.0f}'.format(z), ha='center', va='center', color='white')
#
#     cb = plt.colorbar(imgplot, shrink=0.7)
#     cb.ax.set_yticklabels(cb.ax.get_yticklabels(), fontsize=44)
#     # ff.cmap.set_over('green', alpha=0.3)
#     plt.xticks(range(len(sources)), sources, fontsize=44, rotation=90)
#     plt.yticks(range(len(sources)), sources, fontsize=44)
#
#     plt.ylabel('Source', fontsize=44)
#     plt.xlabel('Target', fontsize=44)
#     fig.set_size_inches(40, 40)
#     plt.tight_layout()
#     plt.savefig('./Figures/' + name + '_' + measure + '.png', dpi=150)


folder = './Results/'
files = [folder+f for f in os.listdir(folder)]
for file in files:
    content = pd.read_csv(file)
    columns = content.columns
    columns = [columns[0]] + [c for c in columns if 's' not in c]

    content = content[columns]
    import pdb
    pdb.set_trace()
    # draw(pickle_file, measure)


