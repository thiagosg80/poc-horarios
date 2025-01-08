from itertools import product


def get_indexes_groups(input, key):
    groups = []
    for container in input:
        indexes = []
        for index, cell in enumerate(container[key]):
            indexes.append(index)
        groups.append(indexes)

    return list(product(*groups))