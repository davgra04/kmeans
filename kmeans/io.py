import numpy


def read_dataset(path):
    print("read_dataset")

    with open(path, "r") as f:

        # determine num dimensions
        ndim = len(f.readline().split(" "))
        print(ndim)

        # seek to beginning of file and slurp with numpy
        data = numpy.fromfile(f, sep=" ")

        # reshape according to ndim
        data = data.reshape(-1, ndim)


    return data


