#!/bin/python3

import sys
import csv
import numpy as np
from sklearn.cluster import KMeans

def main(args):
    header = []
    data = []
    with open(args[0], mode='r', newline='') as infile:
        reader = csv.reader(infile)
        for row in reader:
            if row[0] == 'Date':
                header = row
            else:
                data.append(row)
    data = np.array(data)
    data = np.array(data[:,[4,5,6]])
    print(data)
    with open(args[1], mode='w') as outfile:
        for k in range(3,10):
            kmeans = KMeans(n_clusters=k)
            kmeans.fit(data)
            out = "k:" + str(k) + '\n'
            out += "centers: " + str(kmeans.cluster_centers_) + '\n'
            out += "labels: " + str(kmeans.labels_) + '\n'
            out += "itertia or error: " + str(kmeans.inertia_) + '\n\n'
            outfile.write(out)
    print("\ndone\n\n")

    

if __name__ == "__main__":
    if len(sys.argv) < 3:
        raise SyntaxError("Need input and output file names")
    main(sys.argv[1:])