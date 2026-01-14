import random
from typing import List

from function.get_dias_da_semana import get_dias_da_semana
from turma.function.get_indexes_groups import get_indexes_groups


def get_dias_by_sectors(sectors: List[dict], turmas_do_professor, disponibilidades_by_turno) -> List[dict]:
    dias_da_semana: List[str] = get_dias_da_semana()
    dias_by_sectors: List[dict] = []

    for dia_da_semana in dias_da_semana:
        container_dias: List[dict] = []
        sectors_by_dia_da_semana: List[dict] = [x for x in sectors if x['dia'] == dia_da_semana]
        for turma in turmas_do_professor:
            sectors_by_dia_e_turma: List[dict] = [x for x in sectors_by_dia_da_semana if x['turma'] == turma]
            if sectors_by_dia_e_turma:
                cells: List[dict] = [x['cells'] for x in sectors_by_dia_e_turma]
                container_dias.append({'dia': dia_da_semana, 'turma': turma, 'cells': cells})

        if container_dias:
            indexes_groups = get_indexes_groups(container_dias, 'cells')
            disponibilidade_by_dia = [x for x in disponibilidades_by_turno if x.dia == dia_da_semana][0]
            quantidade_periodos_disponiveis = disponibilidade_by_dia.quantidade_de_periodos

            dia_by_sectors: List[dict] = __get_dia_by_sectors(container_dias, indexes_groups,
                                                              quantidade_periodos_disponiveis)

            dias_by_sectors.append({'dia': dia_da_semana, 'possibilidades': dia_by_sectors})

    return dias_by_sectors


def __get_dia_by_sectors(container_dias, indexes_groups, quantidade_periodos_disponiveis) -> List:
    dias = []
    for indexes in indexes_groups:
        possibilities: dict = {}
        cells: List[dict] = []

        for i, cell_index in enumerate(indexes):
            container = container_dias[i]
            sector = container['cells'][cell_index]

            if __is_possible(sector, cells, quantidade_periodos_disponiveis, i, indexes):
                for cell in sector:
                    cells.append(cell)

                quantidade_periodos_alocados = len([x for x in sector if x['allocated'] != ''])

                possibilities[container['turma']] = {
                    'cells': sector,
                    'quantidade_periodos_alocados': quantidade_periodos_alocados
                }

        if len(possibilities) == len(indexes):
            dias.append(possibilities)

    return dias


def __is_possible(sector, cells, quantidade_periodos_disponiveis, i, indexes) -> bool:
    return (__no_simultaneos_periods(sector, cells) and
            __has_disponibility(cells, sector, quantidade_periodos_disponiveis) and
            __is_allocation_complete(sector, cells, quantidade_periodos_disponiveis, i, indexes))


def __no_simultaneos_periods(sector, cells) -> bool:
    for cell in sector:
        repeated = [x for x in cells if x['periodo'] == cell['periodo'] and x['allocated'] != '' and
                    cell['allocated'] != '']

        if repeated:
            return False

    return True


def __has_disponibility(cells, sector, quantidade_periodos_disponiveis) -> bool:
    return __get_future_cells_quantity(cells, sector) <= quantidade_periodos_disponiveis


def __is_allocation_complete(sector, cells, quantidade_periodos_disponiveis, i, indexes) -> bool:
    is_the_last_sector = i == len(indexes) - 1

    if is_the_last_sector:
        return __get_future_cells_quantity(cells, sector) == quantidade_periodos_disponiveis

    return True


def __get_future_cells_quantity(cells, sector) -> int:
    busy: List[dict] = [x for x in cells if x['allocated'] != '']
    quantidade_de_cells_a_lancar = len([x for x in sector if x['allocated'] != ''])

    return len(busy) + quantidade_de_cells_a_lancar