
from .io import *
from .kmeans import *

def solve_k(path):
    print("solve_k")
    read_dataset(path)
    data = []
    kmeans(data, 1)


