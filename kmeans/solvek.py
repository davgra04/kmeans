from .kmeans import *

def solve_k(data, max_clusters=None, kmeans_iter=5):

    if not max_clusters:
        max_clusters=len(data)//10   # default limit to roughly 10 points per cluster
    print("    max_clusters:", max_clusters)
    print("    kmeans_iter:", kmeans_iter)


    best_sil = np.finfo(np.float).min
    best_grouping = None
    best_centroids = None
    best_k = None


    for k in range(2, max_clusters+1):

        iteration_best_grouping = None
        iteration_best_centroids = None
        iteration_best_sil = np.finfo(np.float).min

        # run kmeans multiple times to yield best silhouette score
        for c in range(kmeans_iter):

            print("        k: {}  iteration: {}\r".format(k, c+1), end="")

            grouping, centroids = kmeans(data, k)

            # calculate average silhouette
            avg_sil = 0
            for d_idx in range(len(data)):
                avg_sil += calculate_silhouette(data, grouping, centroids, d_idx)
                # s = calculate_silhouette(data, grouping, centroids, d_idx)
            avg_sil /= len(data)

            if iteration_best_sil < avg_sil:
                iteration_best_sil = avg_sil
                iteration_best_centroids = centroids
                iteration_best_grouping = grouping

        # update best clustering
        print("        k: {}    iteration_best_sil: {}     ".format(k, iteration_best_sil))
        if best_sil < iteration_best_sil:
            best_sil = iteration_best_sil
            best_grouping = iteration_best_grouping
            best_centroids = iteration_best_centroids
            best_k = k
        # break


    print("    Best k:", best_k)
    print("    Best silhouette score:", best_sil)
    return best_k, best_grouping, best_centroids

def calculate_silhouette(data, grouping, centroids, d_idx):

    # calc mean distance in cluster
    num_points = num_points_in_cluster(grouping, grouping[d_idx])
    if num_points == 1:         # special case
        return 0

    local_cluster = grouping[d_idx]
    sum = 0

    for j_idx in range(len(data)):
        if grouping[j_idx] != local_cluster:   # only consider points in local cluster
            continue
        if j_idx == d_idx:  # skip calculating distance between point and itself
            continue
        sum += (data[d_idx] - data[j_idx]).T @ (data[d_idx] - data[j_idx])
    mean_local_dist = sum / (len(data) - 1)

    # calc min mean distance among other clusters
    #### initialize
    mean_other_dist = np.zeros(len(centroids))

    #### calculate sums
    for j_idx in range(len(data)):
        current_cluster = grouping[j_idx]
        if current_cluster == local_cluster:        # ignore local cluster, only want other clusters
            continue
        mean_other_dist[current_cluster] += (data[d_idx] - data[j_idx]).T @ (data[d_idx] - data[j_idx])

    #### get count of points in each cluster
    num_in_cluster = np.array([num_points_in_cluster(grouping, c_idx) for c_idx in range(len(centroids))])   
    
    #### divide out to get mean distance of each cluster
    # print("mean_other_dist:", mean_other_dist)
    # print("num_in_cluster:", num_in_cluster)
    mean_other_dist /= num_in_cluster

    #### set local cluster to max value (to ignore it for minimum step)
    mean_other_dist[local_cluster] = np.finfo(np.float).max

    # print("local_cluster:", local_cluster)
    # print("mean_other_dist:", mean_other_dist)

    #### extract minimum
    min_mean_other_dist = np.amin(mean_other_dist)
    # print("min_mean_other_dist:", min_mean_other_dist)
    # min_mean_other_dist_idx = np.where(mean_other_dist == min_mean_other_dist)[0][0]
    # print("min_mean_other_dist_idx:", min_mean_other_dist_idx)

    # calc silhouette
    s = (min_mean_other_dist - mean_local_dist) / np.max((mean_local_dist, min_mean_other_dist))
    if s > 1 or s < -1:
        print("GOT A PROBLEM S VALUE:", s)
        print("min_mean_other_dist:", min_mean_other_dist)
        print("mean_local_dist:", mean_local_dist)
    return s


