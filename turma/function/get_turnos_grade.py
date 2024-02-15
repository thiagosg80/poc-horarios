from typing import List

from turma.model.grade.turma import GradeTurma
from turma.model.grade.dia import GradeDia
from turma.model.grade.turno import GradeTurno
from turma.model.turma import Turma


def get_turnos_grade(turmas: List[Turma]) -> List[GradeTurno]:
    turnos_set = list(set(map(lambda t: t.turno, turmas)))
    turnos = list(map(__turno_callback__, turnos_set))
    dias_da_semana = ['seg', 'ter', 'qua', 'qui', 'sex']
    [__set_turnos__(turno, turmas, dias_da_semana) for turno in turnos]

    return turnos


def __turno_callback__(turno: str) -> GradeTurno:
    grade_turno = GradeTurno()
    grade_turno.id = turno

    return grade_turno


def __set_turnos__(turno: GradeTurno, turmas: List[Turma], dias_da_semana: List[str]) -> None:
    turmas_por_turno = list(filter(lambda t: t.turno == turno.id, turmas))
    turnos_dias = list(map(lambda dia: __get_grade_dia__(dia, turmas_por_turno), dias_da_semana))
    turno.dias_da_semana = turnos_dias


def __get_grade_dia__(dia_da_semana: str, turmas: List[Turma]) -> GradeDia:
    grade_dia = GradeDia()
    grade_dia.id = dia_da_semana
    grade_dia.grade_turmas = []
    [__set_aula__(turma, grade_dia) for turma in turmas]

    return grade_dia


def __set_aula__(turma: Turma, grade_dia: GradeDia) -> None:
    grade_turma = GradeTurma()
    grade_turma.id = turma.id
    grade_dia.grade_turmas.append(grade_turma)
