import numpy

def read_dataset(path):

    with open(path, "r") as f:

        # determine num dimensions
        ndim = len(f.readline().split(" "))
        # print(ndim)

        # seek to beginning of file and slurp with numpy
        data = numpy.fromfile(f, sep=" ")

        # reshape according to ndim
        data = data.reshape(-1, ndim)

    return data

def write_solution(path, grouping, centroids):

    with open(path, "w") as f:

        # write k
        f.write("k:\n")
        f.write("{}\n".format(len(centroids)))

        # write centroids
        f.write("centroids:\n")
        for c in centroids:
            c.tofile(f, sep=" ")
            f.write("\n")

        # write grouping
        f.write("grouping:\n")
        for g in grouping:
            g.tofile(f, sep=" ")
            f.write("\n")

