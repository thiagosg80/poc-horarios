import math
import random
from itertools import product

from function.get_converted_grades_by_dia import get_converted_grades_by_dia
from model.sector import Sector
from professor.model.aula import Aula

def get_grades_by_dias(dias_by_sectors: dict, turmas_map, aulas: list[Aula]) -> list[dict]:
    all_possibilities: list[tuple] = __perform_limited_possibilities(dias_by_sectors)
    primeira_aula: Aula = aulas[0]
    turma: str = primeira_aula.turma
    disciplina: str = primeira_aula.disciplina
    quantidade_periodos: int = turmas_map.get(turma).disciplina_map.get(disciplina).quantidade_periodos
    callback = lambda i: __is_valid_possibility(i, quantidade_periodos)
    valid_grades: list[dict] = list(filter(callback, all_possibilities))

    return get_converted_grades_by_dia(valid_grades)

def __perform_limited_possibilities(partial_grade: dict) -> list[tuple]:
    [random.shuffle(possibilidades) for possibilidades in partial_grade.values()]
    possibilidades_total = __get_possibilidades_total(partial_grade)
    limit: int = 10 ** 6
    while possibilidades_total > limit:
        __set_cut(partial_grade)
        possibilidades_total = __get_possibilidades_total(partial_grade)

    return list(product(*list(partial_grade.values())))

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

def __is_valid_possibility(possibility: list[dict], quantidade_periodos: int) -> bool:
    quantidade_periodos_map: dict = {}
    [__set_quantidade_periodos(quantidade_periodos_map, i) for i in possibility]

    return len(list(filter(lambda i: i != quantidade_periodos, quantidade_periodos_map.values()))) == 0

def __set_quantidade_periodos(quantidade_periodos_map: dict, dia: dict) -> None:
    [__set_quantidade_periodos_by_turma(quantidade_periodos_map, turma, sector) for turma, sector in dia.items()]

def __set_quantidade_periodos_by_turma(quantidade_periodos_map: dict, turma: str, sector: Sector) -> None:
    quantidade_periodos_map[turma] = quantidade_periodos_map.get(turma, 0) + sector.quantidade_periodos_alocados