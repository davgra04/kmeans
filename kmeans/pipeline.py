from .io import *
from .solvek import *
import os

def process_dataset(path, max_clusters=None, kmeans_iter=5):
    print("processing", path)

    # read
    data = read_dataset(path)

    # solve
    k, grouping, centroids = solve_k(data, max_clusters=max_clusters, kmeans_iter=kmeans_iter)

    # determine outfile
    path_components = path.split(".")
    new_path = ".".join(path_components[:-1]) + "_{}.".format(k) + path_components[-1]

    # write solution
    print("    writing", new_path)
    write_solution(new_path, grouping, centroids)


def process_all_datasets(dirname="datasets/", max_clusters=None, kmeans_iter=5):

    data_files = []

    for d in os.listdir(dirname):
        if d.endswith(".txt") and "_" not in d:
            data_files.append(dirname + d)


    for d in data_files:
        process_dataset(d, max_clusters=max_clusters, kmeans_iter=kmeans_iter)

