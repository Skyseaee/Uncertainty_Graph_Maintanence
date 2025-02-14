import random
from typing import List


def increase_prob(maps: List[List[int]]) -> List[int]:
    lens = len(maps)
    index1, index2 = -1, -1
    while index1 == index2:
        index1, index2 = random.randint(0, lens-1), random.randint(0, lens-1)

    prob = 0.001
    while prob >= 1:
        prob = maps[index1][index2] - maps[index1][index2] * random.random() + 0.001

    maps[index1][index2], maps[index2][index1] = prob, prob
    return [index1, index2]


def decrease_prob(maps: List[List[int]]) -> List[int]:
    lens = len(maps)
    index1, index2 = -1, -1
    while index1 == index2:
        index1, index2 = random.randint(0, lens), random.randint(0, lens)

    prob = -0.001
    while prob < 0:
        prob = maps[index1][index2] - maps[index1][index2] * random.random() + 0.001

    maps[index1][index2], maps[index2][index1] = prob, prob
    return [index1, index2]


def pipeline_change_map(maps: List[List[int]], increase_or_not: bool) -> List[int]:
    if increase_or_not:
        return increase_prob(maps)
    else:
        return decrease_prob(maps)

