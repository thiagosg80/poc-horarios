from itertools import product, chain

from exception.empty_factor import EmptyFactorException
from function.get_empty_cells import get_empty_cells
from function.get_grades_by_turmas_e_dias import get_grades_by_turmas_e_dias
from professor.model.aula import Aula
from turma.function.get_periodos_ordens import get_periodos_ordens

def get_grades_by_dias(dias_by_sectors: list[dict], turmas_by_turno: list[str], turmas_map, aulas: list[Aula],
                       disponibilidade_map: dict) -> list[dict]:

    factors: dict = __get_factors(turmas_by_turno, turmas_map, aulas, len(dias_by_sectors))
    possibilities_by_turmas: dict = __get_possibilities_by_turmas(dias_by_sectors, turmas_by_turno)

    factored_possibilities = {turma: __get_factored_possibility(turma, factors, possibilities_by_turmas) for turma in
                        turmas_by_turno}

    valid_possibilities_by_turma = {k: __get_valid_possibility_by_turma(v) for k, v in factored_possibilities.items()}

    return get_grades_by_turmas_e_dias(valid_possibilities_by_turma, disponibilidade_map)

def __get_factors(turmas_by_turno: list[str], turmas_map: dict, aulas: list[Aula], quantidade_dias: int) -> dict:
    return {k: __get_factors_by_turma(k, turmas_map, aulas, quantidade_dias) for k in turmas_by_turno}

def __get_factors_by_turma(turma: str, turmas_map: dict, aulas: list[Aula], quantidade_dias: int) -> list[dict]:
    disciplina: str = next(filter(lambda x: x.turma == turma, aulas)).disciplina
    quantidade_periodos: int = turmas_map.get(turma).disciplina_map.get(disciplina).quantidade_periodos
    factors: list[int] = list(range(0, quantidade_periodos + 1))
    factors_by_dias: list[list[int]] = list(map(lambda i: factors, list(range(0, quantidade_dias))))
    all_factors_for_filter: list[tuple] = list(product(*factors_by_dias))
    callback = lambda i: sum(i) == quantidade_periodos

    return list(filter(callback, all_factors_for_filter))

def __get_possibilities_by_turmas(dias: list[dict], turmas: list[str]) -> dict:
    return {turma: __get_sectors_by_turma(turma, dias) for turma in turmas}

def __get_sectors_by_turma(turma: str, dias: list[dict]) -> dict:
    return {d['dia']: __get_sectors_by_dias(d, turma) for d in dias}

def __get_sectors_by_dias(dia: dict, turma: str) -> list[dict]:
    return list(map(lambda i: i.get(turma), dia['possibilidades']))

def __get_by_turma(possibilities: list[dict], turma: str):
    return list(map(lambda p: p[turma], possibilities))

def __get_factored_possibility(turma: str, factors: dict, possibilities_by_turmas: dict) -> list[dict]:
    factor_groups_by_turma: list[tuple] = factors.get(turma)
    possibilities_by_turma: dict = possibilities_by_turmas.get(turma)
    callback = lambda i: __get_possibilities_by_factor_group(i, possibilities_by_turma)
    mapped: list[dict] = list(map(callback, factor_groups_by_turma))

    return list(filter(lambda i: i, mapped))

def __get_possibilities_by_factor_group(factor_group: tuple, possibilities_by_turma: dict) -> dict:
    try:
        return {list(possibilities_by_turma.keys())[k]: __get_possibilities_by_factor(k, v, possibilities_by_turma)
                for k, v in enumerate(factor_group)}
    except EmptyFactorException:
        return {}

def __get_possibilities_by_factor(factor_index: int, factor_value: int, possibilities_by_turma: dict) -> list[dict]:
    callback = lambda x: x['quantidade_periodos_alocados'] == factor_value and x['quantidade_periodos_alocados'] != 0
    all_possibilities_by_factor = list(possibilities_by_turma.values())[factor_index]
    all_quantified = list(filter(callback, all_possibilities_by_factor))

    if len(all_quantified) == 0 and factor_value != 0:
        raise EmptyFactorException

    return __get_unique(all_quantified)

def __get_unique(possibilities: list[dict]) -> list[dict]:
    result: list[dict] = []
    keys: list[tuple] = []
    for possibility in possibilities:
        key: tuple = tuple(cell.allocation for cell in possibility['cells'])
        if key not in keys:
            keys.append(key)
            result.append(possibility)

    return result

def __get_valid_possibility_by_turma(factored_possibilities: list[dict]) -> list[dict]:
    [__handle_empty(i) for i in factored_possibilities]
    possibilities: list[dict] = list(map(lambda i: __get_possibilities(i), factored_possibilities))

    return list(chain.from_iterable(possibilities))

def __handle_empty(possibility: dict) -> None:
    [i.append({'cells': get_empty_cells(get_periodos_ordens())}) for i in possibility.values() if len(i) == 0]

def __get_possibilities(factored_by_group: dict) -> list:
    factored_values: list[list[dict]] = list(factored_by_group.values())
    indexes_groups = __get_indexes_groups(factored_values)
    callback = lambda i: __get_possibilities_by_indexes_groups(i, factored_by_group)

    return list(map(callback, indexes_groups))

def __get_indexes_groups(possibilities: list[list[dict]]) -> list[tuple]:
    ranges: list[int] = list(map(lambda i: list(range(0, len(i))), possibilities))

    return list(product(*ranges))

def __get_possibilities_by_indexes_groups(index_group: tuple, possibilities: dict) -> dict:
    return {list(possibilities.keys())[k]: list(possibilities.values())[k][v] for k, v in enumerate(index_group)}