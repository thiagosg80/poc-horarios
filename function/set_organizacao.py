from typing import List

from professor.model.disponibilidade import Disponibilidade
from professor.model.professor import Professor
from turma.function.fit import fit
from turma.function.get_combine_grades import get_combined_grades
from turma.function.get_cell import get_cell
from turma.function.get_dias_by_sectors import get_dias_by_sectors
from turma.function.get_grades_by_dias import get_grades_by_dias
from turma.function.get_periodos_ordens import get_periodos_ordens
from turma.function.get_sectors import get_sectors


def set_organizacao(professores: List[Professor], turmas_map: dict, grade_template) -> None:
    periodos_ordem = get_periodos_ordens()
    turnos_as_string: set[str] = set(map(lambda x: x.turno, turmas_map.values()))
    grades_by_professor: List[dict] = []

    for professor in professores:
        grades_map: dict = __get_grades_by_professor(professor, turmas_map, periodos_ordem, turnos_as_string)
        grades_by_professor.append({'professor_nome': professor.nome, 'grades': grades_map})

    combined_grades =  get_combined_grades(grades_by_professor, turnos_as_string, turmas_map)
    fit(combined_grades, grade_template)


def __get_grades_by_professor(professor, turmas_map, periodos_ordem, turnos) -> dict:
    grades_map: dict = {}
    __add_grade(grades_map, professor, turmas_map, periodos_ordem, turnos)

    return grades_map


def __add_grade(grades_map, professor, turmas_map, periodos_ordem, turnos) -> None:
    turmas_do_professor: List[str] = list(map(lambda i: i.turma, professor.aulas))

    [__add_grade_by_turno(grades_map, professor, turmas_do_professor, turno, turmas_map, periodos_ordem) for turno in
     turnos]


def __add_grade_by_turno(grades_map, professor, turmas_do_professor, turno, turmas_map, periodos_ordem) -> None:
    turmas_by_turno = __get_turmas_by_turno(turno, turmas_map, turmas_do_professor)

    disponibilidades_by_turno: List[Disponibilidade] = list(filter(lambda i: i.turno == turno,
                                                                   professor.disponibilidades))

    disponibilidade_dias_da_semana = list(map(lambda i: i.dia, disponibilidades_by_turno))
    template = __get_template(disponibilidade_dias_da_semana, turmas_by_turno, periodos_ordem)

    sectors: List[dict] = get_sectors(template, professor, turmas_by_turno, disponibilidade_dias_da_semana,
                                      periodos_ordem)

    dias_by_sectors: List[dict] = get_dias_by_sectors(sectors, turmas_by_turno, disponibilidades_by_turno)
    grades_by_dias = get_grades_by_dias(dias_by_sectors, turmas_by_turno, turmas_map, professor.aulas)
    grades_map[turno] = grades_by_dias


def __get_turmas_by_turno(turno, turmas_map, turmas_do_professor) -> List[str]:
    return list(filter(lambda i: __turmas_by_turno_callback(i, turno, turmas_map), turmas_do_professor))


def __turmas_by_turno_callback(turma_do_professor, turno, turmas_map) -> bool:
    return turmas_map.get(turma_do_professor).turno == turno


def __get_template(dias_da_semana, turmas, periodos_ordem) -> List[dict]:
    cells: List[dict] = []
    for dia in dias_da_semana:
        for turma in turmas:
            for periodo_ordem in periodos_ordem:
                cells.append(get_cell(dia, turma, periodo_ordem))

    return cells