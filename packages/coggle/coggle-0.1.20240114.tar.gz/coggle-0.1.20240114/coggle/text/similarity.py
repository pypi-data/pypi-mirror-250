import math
from difflib import SequenceMatcher
from collections import Counter
from typing import AnyStr


def longest_substr_length(s1: AnyStr, s2: AnyStr) -> int:
    match = SequenceMatcher(None, s1, s2).find_longest_match()
    return match.size


def edit_distance(s1: AnyStr, s2: AnyStr) -> int:
    if len(s1) > len(s2):
        s1, s2 = s2, s1

    distances = range(len(s1) + 1)
    for i2, c2 in enumerate(s2):
        distances_ = [i2+1]
        for i1, c1 in enumerate(s1):
            if c1 == c2:
                distances_.append(distances[i1])
            else:
                distances_.append(
                    1 + min(
                        (distances[i1], distances[i1 + 1], distances_[-1])
                    )
                )
        distances = distances_

    return distances[-1]


def cosine_distance(s1: AnyStr, s2: AnyStr) -> float:
    vec1 = Counter(s1)
    vec2 = Counter(s2)

    intersection = set(vec1.keys()) & set(vec2.keys())
    numerator = sum([vec1[x] * vec2[x] for x in intersection])

    sum1 = sum([vec1[x] ** 2 for x in list(vec1.keys())])
    sum2 = sum([vec2[x] ** 2 for x in list(vec2.keys())])
    denominator = math.sqrt(sum1) * math.sqrt(sum2)

    if not denominator:
        return 1 - 0.0
    else:
        return 1 - float(numerator) / denominator


def jaccard_distance(s1: AnyStr, s2: AnyStr) -> float:
    set_s1 = set(s1)
    set_s2 = set(s2)

    distance = len(set_s1.intersection(set_s2)) / len(set_s1.union(set_s2))
    return 1 - distance


def prefix_length(s1: AnyStr, s2: AnyStr) -> int:
    distance = 0
    for c1, c2 in zip(s1, s2):
        if c1 == c2:
            distance += 1
        else:
            break

    return distance


def hamming_distance(s1: AnyStr, s2: AnyStr) -> int:
    distance = len(s1) - len(s2)
    for c1, c2 in zip(s1, s2):
        if c1 == c2:
            continue
        else:
            distance += 1

    return distance
