import os
import random
from typing import List

DATA_PATH = './data'


def read_file(path: str):
    index = []
    max_prob = .0
    max_index = 0
    with open(path, 'r') as fi:
        lines = fi.readlines()
        for line in lines:
            info = line.split(" ")
            assert (len(info) >= 3 or info[1] == info[2]), "file's format is incorrect."
            v1, v2, prob = int(info[0]), int(info[1]), float(info[2])

            max_prob = max(max_prob, prob)
            max_index = max(max_index, max(v1, v2))
            index.append([v1, v2, prob])

    return index, max_prob, max_index + 1


def construct_map(index: List[List[int]], max_prob: float, max_index: int):
    maps = [[0 for _ in range(max_index)] for _ in range(max_index)]
    for i in index:
        v1, v2, prob = i[0], i[1], i[2]
        # if random.random() < 0.8:
        #     prob = 0
        maps[v1][v2] = prob / max_prob
        maps[v2][v1] = prob / max_prob

    return maps


def pipeline_read_data(filename: str) -> List[List[float]]:
    path = os.path.join(DATA_PATH, filename)
    index, max_prob, max_index = read_file(path)
    return construct_map(index, max_prob, max_index)
