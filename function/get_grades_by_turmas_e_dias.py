import math
import random
from itertools import product


def get_grades_by_turmas_e_dias(partial_grades: dict, disponibilidade_map: dict) -> list[dict]:
    indexes_groups: list[tuple] = __perform_limited_indexes_groups(partial_grades)
    all_combined: list[dict] = list(map(lambda i: __get_combined(i, partial_grades), indexes_groups))

    return list(filter(lambda i: __is_ok(i, disponibilidade_map), all_combined))

def __perform_limited_indexes_groups(partial_grade: dict) -> list[tuple]:
    [random.shuffle(possibilidades) for possibilidades in partial_grade.values()]
    possibilidades_total = __get_possibilidades_total(partial_grade)
    limit: int = 10 ** 6 * 1
    while possibilidades_total > limit:
        __set_cut(partial_grade)
        possibilidades_total = __get_possibilidades_total(partial_grade)

    return __get_indexes_groups(partial_grade)

def __set_cut(partial_grade: dict) -> None:
    major_index: int = __get_major_index(partial_grade)
    fraction: int = math.floor(len(list(partial_grade.values())[major_index]) / 10)
    list(partial_grade.values())[major_index][:fraction] = []

def __get_major_index(partial_grade: dict) -> int:
    possibilidades_lengths: list[int] = list(map(lambda x: len(x), partial_grade.values()))
    max_length: int = max(possibilidades_lengths)
    possibilidades_lengths_map: dict = {len(v): k for k, v in enumerate(partial_grade.values())}

    return possibilidades_lengths_map.get(max_length)

def __get_possibilidades_total(partial_grade: dict) -> int:
    possibilidades_lengths: list[int] = list(map(lambda x: len(x), partial_grade.values()))

    return math.prod(possibilidades_lengths)

def __get_indexes_groups(partial_grade: dict) -> list[tuple]:
    ranges: list[int] = list(map(lambda i: list(range(0, len(i))), partial_grade.values()))

    return list(product(*ranges))

def __get_combined(index_group: tuple[int], partial_grade: dict) -> dict:
    return {list(partial_grade.keys())[k]: list(partial_grade.values())[k][v] for k, v in enumerate(index_group)}

def __is_ok(grade: dict, disponibilidade_map: dict) -> bool:
    return grade.values() and __is_unconflicted(grade) and __is_disponibility_ok(grade, disponibilidade_map)

def __is_unconflicted(grade: dict) -> bool:
    allocated: list[str] = []
    [__add_allocated(allocated, turma) for turma in grade.values()]

    return len(allocated) == len(set(allocated))

def __add_allocated(allocated: list[str], turma: dict) -> None:
    [__add_allocated_by_dia(allocated, dia_key, dia_value) for dia_key, dia_value in turma.items()]

def __add_allocated_by_dia(allocated: list[str], dia_key: str, dia_value: dict) -> None:
    [allocated.append(dia_key + str(cell.position)) for cell in dia_value['cells'] if cell.allocation != '']

def __is_disponibility_ok(grade: dict, disponibilidade_map: dict) -> bool:
    disponibilidade_by_grade: dict = {dia: 0 for dia in disponibilidade_map.keys()}
    [__set_disponibilidade(disponibilidade_by_grade, grade) for grade in grade.values()]
    every_ok: list[bool] = []
    [every_ok.append(disponibilidade_by_grade.get(k) <= disponibilidade_map.get(k)) for k in disponibilidade_map]

    return False not in every_ok

def __set_disponibilidade(disponibilidade_by_grade: dict, grade: dict) -> None:
    [__set_disponibilidade_by_dia(disponibilidade_by_grade, dia, v) for dia, v in grade.items()]

def __set_disponibilidade_by_dia(disponibilidade_by_grade: dict, dia: str, payload_dia: dict) -> None:
    current: int = disponibilidade_by_grade.get(dia)
    disponibilidade_by_grade[dia] = current + payload_dia.get('quantidade_periodos_alocados', 0)