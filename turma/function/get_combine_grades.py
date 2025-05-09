import random
from itertools import product
from typing import List

from function.get_dias_da_semana import get_dias_da_semana
from function.get_disciplinas import get_disciplinas
from turma.function.get_cell import get_cell
from turma.function.get_periodos_ordens import get_periodos_ordens


def get_combined_grades(combined_dias, turnos_as_string, turmas_map) -> dict:
    dias_da_semana: List[str] = get_dias_da_semana()
    periodos_ordens: List[int] = get_periodos_ordens()
    combined_grades: dict = {}
    disciplinas: set[str] = get_disciplinas()

    for turno in turnos_as_string:
        turmas_by_turno = __get_turmas_by_turno(turno, turmas_map)
        dias_by_turno_map: dict = combined_dias[turno]
        container_dias: List[dict] = []
        for dia_da_semana in dias_da_semana:
            if dia_da_semana in dias_by_turno_map:
                container_dias.append({'dia': dia_da_semana, 'possibilidades': dias_by_turno_map[dia_da_semana]})

        combined_grades[turno] = __get_combined_grades(container_dias, turno, turmas_map, periodos_ordens,
                                                       turmas_by_turno, disciplinas)

    return combined_grades


def __get_combined_grades(container_dias, turno, turmas_map, periodos_ordens, turmas_by_turno,
                          disciplinas) -> List[dict]:

    combined_grades: List[dict] = []
    possibilidades_por_dias_e_turmas = __get_possibilidades_por_dias_e_turmas(container_dias)
    acumulado: List[List[dict]] = possibilidades_por_dias_e_turmas[0]
    possibilidades_por_dias_e_turmas.pop(0)

    for index, current in enumerate(possibilidades_por_dias_e_turmas):
        indexes_groups = __get_indexes_groups(acumulado, current)
        acumulado_temp = []
        is_last_day = index == len(possibilidades_por_dias_e_turmas) - 1

        for indexes in indexes_groups:
            to_combine: List[List[dict]] = []
            for key, value in enumerate(indexes):
                partial = acumulado[value] if key == 0 else current[value]
                to_combine.append(partial)

            result: List[dict] = __get_result(to_combine, turmas_by_turno, is_last_day, turmas_map, disciplinas)

            if result:
                acumulado_temp.append(result)

        print(f'Quantidade de grades acumuladas: {len(acumulado_temp)}.')
        acumulado = acumulado_temp

    return combined_grades


def __get_possibilidades_por_dias_e_turmas(container_dias) -> List[List[List[dict]]]:
    converted: List[List[List[dict]]] = []
    for container_dia in container_dias:
        item = [[{'dia': container_dia['dia'], 'turmas': x}] for x in container_dia['possibilidades']]
        converted.append(item)

    return converted


def __get_turmas_by_turno(turno, turmas_map) -> List[str]:
    return list([x for x in turmas_map if turmas_map.get(x).turno == turno])


def __get_indexes_groups(acumulado, current) -> List[tuple]:
    l1 = list(range(len(acumulado)))
    l2 = list(range(len(current)))

    return list(product(l1, l2))

def __get_result(to_combine, turmas_by_turno, is_last_day, turmas_map, disciplinas) -> List[dict]:
    tc1 = to_combine[0]
    tc2 = to_combine[1]
    combined: List[dict] = [*tc1, *tc2]
    for turma_by_turno in turmas_by_turno:
        if not __is_quantity_ok(combined, is_last_day, turma_by_turno, turmas_map, disciplinas):
            return []

    return combined


def __is_quantity_ok(combined, is_last_day, turma_by_turno, turmas_map, disciplinas) -> bool:
    for disciplina in disciplinas:
        quantity_target = turmas_map[turma_by_turno].disciplina_map[disciplina].quantidade_periodos
        current_quantity: int = 0
        for item in combined:
            mapped_turmas = item['turmas']
            if turma_by_turno in mapped_turmas:
                alocados_map = mapped_turmas[turma_by_turno]['quantidade_periodos_alocados']
                if disciplina in alocados_map:
                    current_quantity += alocados_map[disciplina]

        if current_quantity > quantity_target or is_last_day and current_quantity != quantity_target:
            return False

    return True


def __get_cell(container, dia_da_semana, turma_by_turno, periodo_ordem) -> dict:
    if dia_da_semana in container:
        dia = container[dia_da_semana]
        if turma_by_turno in dia:
            return list([x for x in dia[turma_by_turno]['cells'] if x['periodo'] == periodo_ordem])[0]

    return get_cell(dia_da_semana, turma_by_turno, periodo_ordem)