from typing import List

from professor.model.professor import Professor
from turma.model.grade.periodo import Periodo
from turma.model.turma import Turma


def set_organizacao(professores: List[Professor], periodos: List[Periodo], turmas_map: dict) -> None:
    for professor in professores:
        grades_by_professor: List = __get_grades_by_professor(professor, periodos, turmas_map)
    pass


def __get_grades_by_professor(professor, periodos, turmas_map) -> List[dict]:
    grades: List[dict] = []
    __add_grade__(grades, professor, periodos, turmas_map)

    return grades


def __add_grade__(grades, professor, periodos, turmas_map) -> None:
    turnos_as_string: set[str] = set(map(lambda x: x.turno, turmas_map.values()))
    [__add_grade_by_turno__(grades, professor, turno_as_string, turmas_map) for turno_as_string in turnos_as_string]


def __add_grade_by_turno__(grades, professor, turno, turmas_map):
    turmas_as_string: List[str] = list(map(lambda x: x, turmas_map))
    turmas_map_by_turno = []

    for turma_as_string in turmas_as_string:
        turma = turmas_map.get(turma_as_string)
        if turma.turno == turno:
            turmas_map_by_turno.append({'id': turma_as_string, 'meta': turma})
    pass