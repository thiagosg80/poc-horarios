from itertools import combinations
from typing import List

from professor.model.aula import Aula
from turma.function.get_cell import get_cell


def get_sectors(template, professor, turmas, dias, periodos_ordem) -> List[dict]:
    container: List[dict] = []

    for dia in dias:
        for turma in turmas:
            disciplina: str = next(filter(lambda i: i.turma == turma, professor.aulas)).disciplina
            periodos_to_fill = list(filter(lambda i: i['dia'] == dia and i['turma'] == turma, template))
            __add_empty(container, periodos_to_fill, dia, turma)
            aula: Aula = next(filter(lambda i: i.turma == turma and i.disciplina == disciplina, professor.aulas))
            quantidade_maxima_periodos_consecutivos: int = aula.quantidade_maxima_periodos_consecutivos

            for x in range(1, quantidade_maxima_periodos_consecutivos + 1):
                sectors_by_periodos_quantity: List[dict] = []
                all_possible_places: List = list(combinations(range(len(periodos_ordem)), x))
                for indexes in all_possible_places:
                    sector: List[dict] = []
                    allocated_periodos_ordens: List[int] = []
                    for index in indexes:
                        __set_sector(sector, periodos_to_fill, index, dia, turma, professor, disciplina,
                                     allocated_periodos_ordens)

                    if __is_ok(allocated_periodos_ordens):
                        sectors_by_periodos_quantity.append({'dia': dia, 'turma': turma, 'quantidade_periodos': x,
                                                             'cells': sector})

                [container.append(i) for i in sectors_by_periodos_quantity]

    return container


def __add_empty(container, periodos_to_fill, dia, turma) -> None:
    allocations: List[dict] = []
    for periodo_to_fill in periodos_to_fill:
        allocations.append(get_cell(dia, turma, periodo_to_fill['periodo']))

    empty: dict = {'dia': dia, 'turma': turma, 'quantidade_periodos': 0, 'cells': allocations}
    container.append(empty)


def __set_sector(sector, periodos_to_fill, index, dia, turma, professor, disciplina,
                 allocated_periodos_ordens) -> None:

    is_empty: bool = len(sector) == 0
    for x, periodo_to_fill in enumerate(periodos_to_fill):
        description: str = professor.nome + ' - ' + disciplina if x == index else ''
        if is_empty:
            cell: dict = get_cell(dia, turma, periodo_to_fill['periodo'])
            cell['allocated'] = description
            sector.append(cell)
            if description:
                allocated_periodos_ordens.append(cell['periodo'])
        else:
            if description:
                sector[x]['allocated'] = description
                allocated_periodos_ordens.append(sector[x]['periodo'])


def __is_ok(allocated_periodos_ordens: List[int]) -> bool:
    allocated_count = len(allocated_periodos_ordens)

    return (allocated_count == 1 or allocated_count == 2 or
            allocated_count > 2 and len([x for x in allocated_periodos_ordens if x in [1, 3, 5]]) != 3)