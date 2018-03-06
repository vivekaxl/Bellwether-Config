from __future__ import division
import pickle
import os
import pandas as pd
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches


def draw(heatmap_arr, xlabel, name):
    # mapping = {
    #     "Better": 1,
    #     "Same": 0.5,
    #     "Worse": 0
    # }
    # fig, ax = plt.subplots()
    # Using matshow here just because it sets the ticks up nicely. imshow is faster.
    tt = []
    sources = []
    for ha in heatmap_arr:
        print ha[0], ha
        sources.append(ha[0])
        tt.append(ha[1:])

    # imgplot = ax.matshow(tt, cmap="Pastel2")

    from matplotlib.colors import ListedColormap

    fig, ax = plt.subplots()
    # discrete color scheme
    # cMap = ListedColormap([ '#beaed4', '#fdc086','#7fc97f'])
    heatmap = ax.pcolor(np.array(tt), edgecolors='white', linewidths=6, vmin=0, vmax=1)

    # legend
    cbar = plt.colorbar(heatmap)
    # Manually specify colorbar labelling after it's been generated
    cbar.ax.tick_params(labelsize=44)
    cbar.set_ticks([1, 0.5, 0])
    cbar.set_ticklabels(['Better', 'Same', 'Worse'])
    #
    # cbar.ax.get_yaxis().set_ticks([])
    # for j, lab in enumerate([ 'Same', 'Worse', 'Better',]):
    #     cbar.ax.text(.5, (2 * j + 1) / 6.0, lab, ha='center', va='center', fontsize=44, color='black')

    # box = ax.get_position()
    # ax.set_position([box.x0, box.y0, box.width * 0.7, box.height])
    # legend_ax = fig.add_axes([.7, .5, 1, .1])
    # legend_ax.axis('off')
    # colors = plt.cm.Pastel2(np.linspace(0, 1, len(mapping)))
    # patches = [mpatches.Patch(facecolor=c, edgecolor=c) for c in colors]
    # legend = legend_ax.legend(patches,
    #                           sorted(mapping),
    #                           handlelength=0.8, loc='lower left')
    # for t in legend.get_texts():
    #     t.set_ha("left")
    #
    # # cb = plt.colorbar(imgplot, shrink=0.7)
    # # cb.ax.set_yticklabels(cb.ax.get_yticklabels(), fontsize=44)
    # # ff.cmap.set_over('green', alpha=0.3)
    plt.xticks([x+0.5 for x in range(len(xlabel))], xlabel, fontsize=44)
    plt.yticks([x+0.5 for x in range(len(sources))], sources, fontsize=44)
    #
    plt.ylabel('Software Systems', fontsize=44)
    plt.xlabel('Target Training Percentage', fontsize=44)
    fig.set_size_inches(40, 40)
    plt.tight_layout()
    plt.savefig('./Figures/' + name + '.png', dpi=150)


folder = './Results/'
files = [folder+f for f in os.listdir(folder)]
# files = ['./Results_10-100/storm-obj2.csv']

for file in files:
    name = file.split('/')[-1].replace('.csv', '')
    content = pd.read_csv(file)
    columns = content.columns
    content = content.sort('Target Files')
    columns = [columns[0]] + [c for c in columns[1:] if 's' in c]
    labels = [c for c in content.columns if 's' not in c]
    content = content[columns]
    listoflist = content.values.tolist()
    tlistoflist = []
    for ll in listoflist:
        t = [ll[0]]
        print ll
        for l in ll[1:]:
            if l == 'better': t.append(1)
            elif l == 'same': t.append(0.5)
            elif l == 'worse': t.append(0)
            else:
                print ">", l
                print "Error"
                import pdb
                pdb.set_trace()
                exit()
        assert(len(t) == len(ll)), "Something is wrong"
        assert(len(t)-1 == len(labels)), "Something is wrong"
        tlistoflist.append(t)
    draw(tlistoflist, labels, name)




