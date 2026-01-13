from itertools import product

from model.sector import Sector


def get_dias_by_sectors(sectors: list[Sector], turmas_do_professor, disponibilidade_dias_da_semana: list[str],
                        quantidades_periodos_map: dict, disponibilidade_map: dict) -> dict:

    all_days: dict = {d: __get_days(d, sectors, turmas_do_professor) for d in disponibilidade_dias_da_semana}
    all_possibilities: dict = {d: __get_possibilities(all_days.get(d)) for d in disponibilidade_dias_da_semana}
    first_mapped: dict = list(quantidades_periodos_map.values())[0]
    quantidade_minima_periodos_consecutivos: int = first_mapped['quantidade_minima_periodos_consecutivos']

    ok_possibilities: dict = {d: __get_ok_possibilities(all_possibilities.get(d),
                                                        quantidade_minima_periodos_consecutivos,
                                                        disponibilidade_map.get(d)) for d in
                              disponibilidade_dias_da_semana}

    return {d: __get_mapped_by_turma(ok_possibilities.get(d)) for d in disponibilidade_dias_da_semana}

def __get_days(dia: str, sectors: list[Sector], turmas: list[str]) -> dict:
    return {t: list(filter(lambda i: i.turma == t and i.dia == dia, sectors)) for t in turmas}

def __get_possibilities(days: dict) -> list[dict]:
    return list(product(*list(days.values())))

def __get_ok_possibilities(possibilities: list[tuple], quantidade_minima_periodos_consecutivos: int,
                           quantidade_periodos_disponibilidade: int) -> list[dict]:

    callback = lambda i: __is_ok(i, quantidade_minima_periodos_consecutivos, quantidade_periodos_disponibilidade)

    return list(filter(callback, possibilities))

def __is_ok(possibility: tuple, quantidade_minima_periodos_consecutivos: int,
            quantidade_periodos_disponibilidade: int) -> bool:

    return (__is_unconflicted(possibility)
            and __has_enought_disponibility(possibility, quantidade_periodos_disponibilidade)
            and __is_ok_quantidade_minima_periodos_consecutivos(possibility, quantidade_minima_periodos_consecutivos))

def __is_unconflicted(possibility: tuple) -> bool:
    allocated: list[str] = []
    [__add_allocated(allocated, sector) for sector in possibility]

    return len(allocated) == len(set(allocated))

def __add_allocated(allocated: list[str], sector: Sector) -> None:
    [allocated.append(sector.dia + str(cell.position)) for cell in sector.cells if cell.allocation != '']

def __has_enought_disponibility(possibility: tuple[Sector], quantidade_periodos_disponibilidade: int) -> bool:
    quantidade_alocada: int = sum(list(map(lambda x: x.quantidade_periodos_alocados, possibility)))

    return quantidade_alocada <= quantidade_periodos_disponibilidade

def __is_ok_quantidade_minima_periodos_consecutivos(possibility: tuple[Sector],
                                                    quantidade_minima_periodos_consecutivos: int) -> bool:

    callback = lambda i: (i.quantidade_periodos_alocados != 0
                          and i.quantidade_periodos_alocados < quantidade_minima_periodos_consecutivos)

    not_enought: list[Sector] = list(filter(callback, possibility))

    return len(not_enought) < quantidade_minima_periodos_consecutivos

def __get_mapped_by_turma(possibilities: list[tuple]) -> list[dict]:
    return list(map(lambda i: __get_mapped(i), possibilities))

def __get_mapped(possibility: tuple[Sector]) -> dict:
    return {s.turma: s for s in possibility}