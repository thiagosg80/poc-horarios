from itertools import product
from typing import List

from function.get_dias_da_semana import get_dias_da_semana
from turma.function.get_cell import get_cell
from turma.function.get_periodos_ordens import get_periodos_ordens


def get_combined_dias(grades_by_professor, turnos_as_string, turmas_map) -> dict:
    dias_da_semana: List[str] = get_dias_da_semana()
    periodos_ordens: List[int] = get_periodos_ordens()
    combined_grades: dict = {}
    for turno in turnos_as_string:
        turmas_by_turno = __get_turmas_by_turno(turno, turmas_map)
        combined_grades[turno]: dict = {}
        for dia_da_semana in dias_da_semana:
            possibilidades_por_professor_e_dia = []
            for grade_professor in grades_by_professor:
                possibilidades_por_turno = grade_professor['possibilidades'][turno]
                if dia_da_semana in possibilidades_por_turno:
                    possibilidades_por_professor_e_dia.append(possibilidades_por_turno[dia_da_semana])

            if possibilidades_por_professor_e_dia:
                combined_grades[turno][dia_da_semana] = __get_combined_dias(possibilidades_por_professor_e_dia,
                                                                            dia_da_semana, turmas_by_turno,
                                                                            periodos_ordens)

    return combined_grades


def __get_turmas_by_turno(turno, turmas_map) -> List[str]:
    return list([x for x in turmas_map if turmas_map.get(x).turno == turno])


def __get_combined_dias(possibilidades_por_professor_e_dia, dia_da_semana, turmas_by_turno,
                        periodos_ordens) -> List[dict]:

    acumulado: List[dict] = possibilidades_por_professor_e_dia[0]
    possibilidades_por_professor_e_dia.pop(0)
    for current in possibilidades_por_professor_e_dia:
        indexes_groups = __get_indexes_groups(acumulado, current)
        acumulado_temp = []

        for indexes in indexes_groups:
            to_combine: List[dict] = []
            for key, value in enumerate(indexes):
                partial = acumulado[value] if key == 0 else current[value]
                to_combine.append(partial)

            result = __get_result(to_combine, dia_da_semana, turmas_by_turno, periodos_ordens)

            if result:
                acumulado_temp.append(result)

        acumulado = acumulado_temp

    return acumulado


def __get_indexes_groups(combined, current_grade) -> List[tuple]:
    l1 = list(range(len(combined)))
    l2 = list(range(len(current_grade)))

    return list(product(l1, l2))


def __get_result(to_combine, dia_da_semana, turmas_by_turno, periodos_ordens) -> dict:
    result_turma: dict = {}
    for turma_by_turno in turmas_by_turno:
        result_sector: List[dict] = []
        for periodo_ordem in periodos_ordens:
            cell_p1 = __get_cell(to_combine[0], dia_da_semana, turma_by_turno, periodo_ordem)
            cell_p2 = __get_cell(to_combine[1], dia_da_semana, turma_by_turno, periodo_ordem)

            if cell_p1['allocated'] and cell_p2['allocated']:
                return {}

            result_sector.append(cell_p1) if cell_p1['allocated'] else result_sector.append(cell_p2)
        result_turma[turma_by_turno] = {'cells': result_sector}

    return result_turma

def __get_cell(container, dia_da_semana, turma_by_turno, periodo_ordem) -> dict:
    if turma_by_turno in container:
        return list([x for x in container[turma_by_turno]['cells'] if x['periodo'] == periodo_ordem])[0]

    return get_cell(dia_da_semana, turma_by_turno, periodo_ordem)