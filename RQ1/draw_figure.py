from __future__ import division
import pickle
import sys
import numpy as np
import matplotlib as mpl


def draw(pickle_file, measure):
    import matplotlib.pyplot as plt
    name = pickle_file.split('/')[-1].replace('.p', '')
    content = pickle.load(open(pickle_file))
    sources = sorted(content.keys())

    max_num = sys.maxint * -1
    heatmap_arr = []
    for source in sources:
        t = []
        for target in sources:

            try:
                t.append(np.median(content[source][target][measure]))
                max_num = max(max_num, t[-1])
            except:
                t.append(1000000)
        heatmap_arr.append(t)

    # # remove outliers
    # for i, h in enumerate(heatmap_arr):
    #     m = sum([hhh for hhh in h if 2000 != hhh]) / (len(h) - 1)
    #     for j, hh in enumerate(h):
    #         if hh > 4000:
    #             heatmap_arr[i][j] = 8000

    # imgplot = plt.imshow(heatmap_arr, cmap='seismic', interpolation='nearest')
    # plt.xticks(range(len(sources)), sources, fontsize=12, rotation=90)
    # plt.yticks(range(len(sources)), sources, fontsize=12)
    # plt.colorbar(imgplot)
    # plt.show()

    fig, ax = plt.subplots()
    # Using matshow here just because it sets the ticks up nicely. imshow is faster.
    imgplot = ax.matshow(heatmap_arr, cmap='Greys', vmax=max_num)
    ax.set_xticks(np.arange(-.5, len(sources), 1), minor=True);
    ax.set_yticks(np.arange(-.5, len(sources), 1), minor=True);

    ax.grid(which='minor',color='w', linestyle='-', linewidth=6)

    for i in xrange(len(heatmap_arr)):
        ax.add_patch(mpl.patches.Rectangle((i - .5, i - .5), 1, 1, hatch='+/', fill=False, snap=False, color='red', linewidth=8))

    for (i, j), z in np.ndenumerate(heatmap_arr):
        if z == 1000000:
            # ax.text(j, i, 'X', ha='center', va='center', color='black')
            pass
        else:
            ax.text(j, i, round(z, 2), ha='center', va='center', color='black', fontsize=28)

    cb = plt.colorbar(imgplot, shrink=0.7)
    cb.ax.set_yticklabels(cb.ax.get_yticklabels(), fontsize=44)
    # ff.cmap.set_over('green', alpha=0.3)
    plt.xticks(range(len(sources)), sources, fontsize=44, rotation=90)
    plt.yticks(range(len(sources)), sources, fontsize=44)

    plt.ylabel('Source', fontsize=44)
    plt.xlabel('Target', fontsize=44)
    fig.set_size_inches(40, 40)
    plt.savefig('./Figures/normalized-' + name + '_' + measure + '.png', dpi=150)


pickle_folder = './Processed/'
pickle_files = [
    './Processed/spear.p',
    './Processed/sac.p',
    './Processed/sqlite.p',
    './Processed/x264.p',
    './Processed/storm-obj1.p',
    './Processed/storm-obj2.p'
]

measures = ['rank']#, 'mmre', 'abs_res']
for measure in measures:
    for pickle_file in pickle_files:
        draw(pickle_file, measure)


