from itertools import product
from typing import List


def get_indexes_groups(groups_input, key) -> List[tuple]:
    groups = []
    for container in groups_input:
        indexes = []
        for index, cell in enumerate(container[key]):
            indexes.append(index)
        groups.append(indexes)

    return list(product(*groups))