from itertools import combinations, chain
from typing import List

from function.get_empty_sector import get_empty_sector
from model.cell import Cell
from model.sector import Sector
from professor.model.aula import Aula
from professor.model.professor import Professor


def get_sectors(professor: Professor, turmas_by_turno: List[str], disponibilidade_dias_da_semana: List[str],
                turno: str, periodos_ordens: List[int]) -> List[Sector]:

    callback = lambda i: __get_sectors_by_disponibilidade(i, turno, professor, turmas_by_turno, periodos_ordens)
    result_map: map = map(callback, disponibilidade_dias_da_semana)
    all_sectors_by_disponibilidade_raw: List[List[Sector]] = list(result_map)
    all_sectors_by_disponibilidade: List[Sector] = list(chain.from_iterable(all_sectors_by_disponibilidade_raw))
    turmas_map: dict = __get_turmas_map(professor.aulas)
    sectors: List[Sector] = list(filter(lambda i: __is_ok(i, turmas_map), all_sectors_by_disponibilidade))
    __add_empty(sectors, turmas_by_turno, disponibilidade_dias_da_semana, periodos_ordens)

    return sectors


def __get_sectors_by_disponibilidade(dia_disponibilidade: str, turno: str, professor: Professor,
                                     turmas: List[str], periodos_ordens: List[int]) -> List[Sector]:

    filtered: filter = filter(lambda i: i.turno == turno and i.dia == dia_disponibilidade, professor.disponibilidades)
    quantidade_periodos_disponiveis: int = next(filtered).quantidade_de_periodos
    quantidades_periodos: range = range(1, quantidade_periodos_disponiveis + 1)
    callback = lambda i: __get_setores_by_disponibilidade(i, professor, dia_disponibilidade, turmas, periodos_ordens)
    mapped: map = map(callback, quantidades_periodos)
    result: List[List[Sector]] = list(mapped)

    return list(chain.from_iterable(result))


def __get_setores_by_disponibilidade(quantidade_disponivel: int, professor: Professor, dia: str,
                                     turmas: List[str], periodos_ordens: List[int]) -> List[Sector]:

    callback = lambda i: __get_setores_by_turma(i, professor, dia, quantidade_disponivel, periodos_ordens)
    mapped: map = map(callback, turmas)
    result: List[List[Sector]] = list(mapped)

    return list(chain.from_iterable(result))


def __get_setores_by_turma(turma: str, professor: Professor, dia: str, quantidade_disponivel: int,
                           periodos_ordens: List[int]) -> List[Sector]:

    combinacoes: List[tuple] = list(combinations(periodos_ordens, quantidade_disponivel))
    mapped: map = map(lambda i: __get_filled_sector(i, periodos_ordens, professor, dia, turma), combinacoes)

    return list(mapped)


def __get_filled_sector(combination: tuple, periodos_ordens: List[int], professor: Professor, dia: str,
                        turma: str) -> Sector:

    sector: Sector = get_empty_sector(periodos_ordens)
    sector.dia = dia
    sector.turma = turma
    [__set_allocation(sector.cells, number - 1, professor) for number in combination]

    return sector


def __set_allocation(cells: List[Cell], position: int, professor: Professor) -> None:
    cells[position].allocation = professor.nome + ' - ' + professor.disciplina


def __get_turmas_map(aulas: List[Aula]) -> dict:
    return {aula.turma: {'quantidade_maxima_periodos_consecutivos': aula.quantidade_maxima_periodos_consecutivos,
                         'quantidade_minima_periodos_consecutivos': aula.quantidade_minima_periodos_consecutivos}
            for aula in aulas}


def __is_ok(sector: Sector, turmas_map: dict) -> bool:
    turma: str = sector.turma
    maxima: int = turmas_map.get(turma)['quantidade_maxima_periodos_consecutivos']
    cells: List[Cell] = sector.cells
    allocated: List[Cell] = list(filter(lambda i: i.allocation != '', cells))
    allocated_positions: List[int] = list(map(lambda x: x.position, allocated))

    return __is_ok_quantidade_maxima_periodos_consecutivos(allocated_positions, maxima)


def __is_ok_quantidade_maxima_periodos_consecutivos(allocated_positions: List[int], maxima: int) -> bool:
    quantity_allocated: int = len(allocated_positions)

    return quantity_allocated <= maxima or not __is_sequence(allocated_positions)


def __is_sequence(values: List[int]) -> bool:
    first: int = values[0]

    return values == list(range(first, first + len(values)))


def __add_empty(container: List[Sector], turmas_by_turno: List[str], disponibilidade_dias_da_semana: List[str],
                periodos_ordens: List[int]) -> None:

    callback = lambda i: __get_empty_by_turma(i, disponibilidade_dias_da_semana, periodos_ordens)
    nested: List[List[Sector]] = list(map(callback, turmas_by_turno))
    empty_sectors: List[Sector] = list(chain.from_iterable(nested))
    [container.append(empty_sector) for empty_sector in empty_sectors]


def __get_empty_by_turma(turma: str, disponibilidade_dias_da_semana: List[str],
                         periodos_ordens: List[int]) -> List[Sector]:

    callback = lambda i: __get_empty_by_disponibilidade(i, turma, periodos_ordens)

    return list(map(callback, disponibilidade_dias_da_semana))


def __get_empty_by_disponibilidade(dia: str, turma: str, periodos_ordens: List[int]) -> Sector:
    sector: Sector = get_empty_sector(periodos_ordens)
    sector.dia = dia
    sector.turma = turma

    return sector