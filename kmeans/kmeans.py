import numpy as np
import random

# adjust_grouping updates the grouping array such that each data point is grouped
# with the nearest centroid
def adjust_grouping(data, grouping, centroids):

    # find closest cluster center for each data point
    for d_idx in range(len(data)):

        d = data[d_idx]
        min_dist = np.finfo(np.float).max
        min_c_idx = 0

        # check distance each center, keep track of minimum
        for c_idx in range(len(centroids)):
            c = centroids[c_idx]
            dist = (d - c).T @ (d - c)

            if dist < min_dist:
                min_dist = dist
                min_c_idx = c_idx
        
        # update grouping
        grouping[d_idx] = min_c_idx


# adjust_centroids updates the centroid positions in order to minimize the objective
# function (minimize euclidean distance between centroid and points in group)
def adjust_centroids(data, grouping, centroids):

    for c_idx in range(len(centroids)):
        c = centroids[c_idx]
        num_pts = num_points_in_cluster(grouping, c_idx)

        # if no points in this cluster, randomly set center to another cluster's center
        if num_pts == 0:            
            # move centroid to location of a random data point
            # print("NO POINTS IN CLUSTER")
            centroids[c_idx] = data[random.randint(0, len(data)-1)]

            continue

        # still have points in cluster, calculate new position
        sum = np.zeros(data[0].shape)
        for d_idx in range(len(data)):
            if grouping[d_idx] != c_idx:    # skip data points not in cluster
                continue
            sum += data[d_idx]
        centroids[c_idx] = 1 / num_pts * sum


# num_points_in_cluster returns the number of data points within a specified cluster
def num_points_in_cluster(grouping, c_idx):
    count = 0
    for c in grouping:
        if c == c_idx:
            count += 1
    return count


# kmeans clusters the given data points into k clusters
#   data - The data array to cluster
#   k - number of clusters to create
#   threshold - number of consecutive iterations for the clustering to remain stable
#               in order to be considered converged
#   init - initialization method for clusters, must be "random_assignment" or "forgy"
def kmeans(data, k, threshold=10, init="random_assignment"):

    # initialize centroids and grouping
    if init == "random_assignment":
        centroids = np.tile(np.zeros(data[0].shape), (k,1))
        grouping = np.random.randint(low=0, high=k, size=len(data))
        adjust_centroids(data, grouping, centroids)
    elif init == "forgy":
        index = np.random.choice(data.shape[0], k, replace=False)  
        centroids = data[index]               # cluster centroids
        grouping = np.zeros(len(data), dtype=np.int)      # assignment of data point to cluster
    else:
        raise ValueError("{} unrecognized. init must be either \"random_assignment\" or \"forgy\"!".format(init))

    # iterate until clusters have converged
    converged = False
    conv_count = 0

    while not converged:
        # save previous state
        previous_grouping = grouping.copy()

        # iterate grouping and cluster centroids
        adjust_grouping(data, grouping, centroids)
        adjust_centroids(data, grouping, centroids)

        # check if converged
        if (grouping == previous_grouping).all():
            conv_count += 1
            if conv_count == threshold:
                converged = True
        else:
            conv_count = 0

    return grouping, centroids



