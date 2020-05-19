import numpy as np


def adjust_grouping(data, grouping, centers):

    # find closest cluster center for each data point
    for d_idx in range(len(data)):

        d = data[d_idx]
        min_dist = np.finfo(np.float).max
        min_c_idx = 0

        # check distance each center, keep track of minimum
        for c_idx in range(len(centers)):
            c = centers[c_idx]
            dist = (d - c).T @ (d - c)

            if dist < min_dist:
                min_dist = dist
                min_c_idx = c_idx
        
        # update grouping
        grouping[d_idx] = min_c_idx



def adjust_centers(data, grouping, centers):

    for c_idx in range(len(centers)):
        c = centers[c_idx]
        num_pts = num_points_in_cluster(grouping, c_idx)

        # if no points in this cluster, randomly set center to another cluster's center
        if num_pts == 0:
            print("NO POINTS IN THIS CLUSTER")
            old_c = c
            while (old_c == centers[c_idx]).all():
                centers[c_idx] = centers[random.randint(0, len(centers)-1)]
            continue

        # still have points in cluster, update position
        sum = np.zeros(data[0].shape)
        for d_idx in range(len(data)):
            if grouping[d_idx] != c_idx:    # skip data points not in cluster
                continue
            sum += data[d_idx]

        new_c = 1 / num_pts * sum

        # print("new_c:", new_c)

        centers[c_idx] = new_c



def num_points_in_cluster(grouping, c_idx):
    count = 0
    for c in grouping:
        if c == c_idx:
            count += 1
    return count

def kmeans(data, k, threshold=100):

    # randomly initialize cluster centers from data
    npoints = len(data)
    ndim = len(data[0])
    print("npoints:", npoints)
    print("ndim:", ndim)
    print("k:", k)

    index = np.random.choice(data.shape[0], k, replace=False)  

    centers = data[index]               # cluster centers
    grouping = np.zeros(len(data))      # assignment of data point to cluster

    print("index:", index)
    print("centers:\n", centers)


    converged = False
    conv_count = 0

    while not converged:
        # save previous state
        previous_grouping = grouping.copy()

        # iterate grouping and cluster centers
        adjust_grouping(data, grouping, centers)
        adjust_centers(data, grouping, centers)

        # check if converged
        if (grouping == previous_grouping).all():
            conv_count += 1
            if conv_count == threshold:
                converged = True
        else:
            conv_count = 0


    print("done")
    print(grouping)




    # dummy output
    # grouping = np.zeros(len(data))

    # for i in range(len(data)//2, len(data)):
    #     grouping[i] = 1

    return grouping, centers



