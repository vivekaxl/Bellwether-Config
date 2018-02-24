import os

files = [f for f in os.listdir('.') if '.csv' in f]

for file in sorted(files):
    c = open(file).readline()
    tc = open(file).readlines()
    print file, len(c.split(','))-1, len(tc)-1
