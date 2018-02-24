from sk import rdivDemo
import os

folder = "./Results/"
results = [folder+f for f in os.listdir(folder) if '.csv' in f]

for result in results:
    content = open(result).readlines()
    content = content[1:]
    l = []
    for c in content:
        c = c.split(',')
        l.append([c[0]] + map(float, c[1:]))
    family_name = result.split('/')[-1].replace('.csv', '')
    rdivDemo(family_name, l, globalMinMax=False, isLatex=True)