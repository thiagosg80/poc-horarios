from itertools import combinations, chain

from function.get_empty_sector import get_empty_sector
from model.cell import Cell
from model.sector import Sector
from professor.model.professor import Professor


def get_sectors(professor: Professor, turmas_by_turno: list[str], disponibilidade_dias_da_semana: list[str],
                turno: str, periodos_ordens: list[int], quantidades_periodos_map: dict) -> list[Sector]:

    callback = lambda i: __get_sectors_by_disponibilidade(i, turno, professor, turmas_by_turno, periodos_ordens)
    result_map: map = map(callback, disponibilidade_dias_da_semana)
    all_sectors_by_disponibilidade_raw: list[list[Sector]] = list(result_map)
    all_sectors_by_disponibilidade: list[Sector] = list(chain.from_iterable(all_sectors_by_disponibilidade_raw))
    is_ok_callback = lambda i: __is_ok(i, quantidades_periodos_map)
    sectors: list[Sector] = list(filter(is_ok_callback, all_sectors_by_disponibilidade))
    __add_empty(sectors, turmas_by_turno, disponibilidade_dias_da_semana, periodos_ordens)

    return sectors

def __get_sectors_by_disponibilidade(dia_disponibilidade: str, turno: str, professor: Professor,
                                     turmas: list[str], periodos_ordens: list[int]) -> list[Sector]:

    filtered: filter = filter(lambda i: i.turno == turno and i.dia == dia_disponibilidade, professor.disponibilidades)
    quantidade_periodos_disponiveis: int = next(filtered).quantidade_de_periodos
    quantidades_periodos: range = range(1, quantidade_periodos_disponiveis + 1)
    callback = lambda i: __get_setores_by_disponibilidade(i, professor, dia_disponibilidade, turmas, periodos_ordens)
    mapped: map = map(callback, quantidades_periodos)
    result: list[list[Sector]] = list(mapped)

    return list(chain.from_iterable(result))

def __get_setores_by_disponibilidade(quantidade_disponivel: int, professor: Professor, dia: str,
                                     turmas: list[str], periodos_ordens: list[int]) -> list[Sector]:

    callback = lambda i: __get_setores_by_turma(i, professor, dia, quantidade_disponivel, periodos_ordens)
    mapped: map = map(callback, turmas)
    result: list[list[Sector]] = list(mapped)

    return list(chain.from_iterable(result))

def __get_setores_by_turma(turma: str, professor: Professor, dia: str, quantidade_disponivel: int,
                           periodos_ordens: list[int]) -> list[Sector]:

    combinacoes: list[tuple] = list(combinations(periodos_ordens, quantidade_disponivel))
    mapped: map = map(lambda i: __get_filled_sector(i, periodos_ordens, professor, dia, turma), combinacoes)

    return list(mapped)

def __get_filled_sector(combination: tuple, periodos_ordens: list[int], professor: Professor, dia: str,
                        turma: str) -> Sector:

    sector: Sector = get_empty_sector(periodos_ordens)
    sector.dia = dia
    sector.turma = turma
    [__set_allocation(sector.cells, number - 1, professor) for number in combination]

    return sector

def __set_allocation(cells: list[Cell], position: int, professor: Professor) -> None:
    cells[position].allocation = professor.nome + ' - ' + professor.disciplina

def __is_ok(sector: Sector, quantidades_periodos_map: dict) -> bool:
    turma: str = sector.turma
    maxima: int = quantidades_periodos_map.get(turma)['quantidade_maxima_periodos_consecutivos']
    minima: int = quantidades_periodos_map.get(turma)['quantidade_minima_periodos_consecutivos']
    cells: list[Cell] = sector.cells
    allocated: list[Cell] = list(filter(lambda i: i.allocation != '', cells))
    allocated_positions: list[int] = list(map(lambda x: x.position, allocated))

    return (__is_ok_quantidade_maxima_periodos_consecutivos(allocated_positions, maxima)
            and __is_ok_pre_quantidade_minima_periodos_consecutivos(allocated_positions, minima))

def __is_ok_quantidade_maxima_periodos_consecutivos(allocated_positions: list[int], maxima: int) -> bool:
    quantity_allocated: int = len(allocated_positions)

    return quantity_allocated <= maxima or not __is_sequence(allocated_positions)

def __is_ok_pre_quantidade_minima_periodos_consecutivos(allocated_positions: list[int], minima: int) -> bool:
    quantity_allocated: int = len(allocated_positions)

    return quantity_allocated != minima or  __is_sequence(allocated_positions)

def __is_sequence(values: list[int]) -> bool:
    first: int = values[0]

    return values == list(range(first, first + len(values)))

def __add_empty(container: list[Sector], turmas_by_turno: list[str], disponibilidade_dias_da_semana: list[str],
                periodos_ordens: list[int]) -> None:

    callback = lambda i: __get_empty_by_turma(i, disponibilidade_dias_da_semana, periodos_ordens)
    nested: list[list[Sector]] = list(map(callback, turmas_by_turno))
    empty_sectors: list[Sector] = list(chain.from_iterable(nested))
    [container.append(empty_sector) for empty_sector in empty_sectors]

def __get_empty_by_turma(turma: str, disponibilidade_dias_da_semana: list[str],
                         periodos_ordens: list[int]) -> list[Sector]:

    callback = lambda i: __get_empty_by_disponibilidade(i, turma, periodos_ordens)

    return list(map(callback, disponibilidade_dias_da_semana))

def __get_empty_by_disponibilidade(dia: str, turma: str, periodos_ordens: list[int]) -> Sector:
    sector: Sector = get_empty_sector(periodos_ordens)
    sector.dia = dia
    sector.turma = turma

    return sector