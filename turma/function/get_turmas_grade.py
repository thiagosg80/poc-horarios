from typing import List

from turma.model.grade.aula import Aula
from turma.model.grade.dia import TurnoDia
from turma.model.grade.grade import TurmaGrade
from turma.model.grade.turno import GradeTurno
from turma.model.turma import Turma


def get_turmas_grade(turmas: List[Turma]) -> TurmaGrade:
    grade = TurmaGrade()
    turnos = list(set(map(lambda t: t.turno, turmas)))
    grade.turnos = list(map(__turno_callback__, turnos))
    dias_da_semana = ['seg', 'ter', 'qua', 'qui', 'sex']
    [__set_turnos__(turno, turmas, dias_da_semana) for turno in grade.turnos]

    return grade


def __turno_callback__(turno: str) -> GradeTurno:
    grade_turno = GradeTurno()
    grade_turno.id = turno

    return grade_turno


def __set_turnos__(turno: GradeTurno, turmas: List[Turma], dias_da_semana: List[str]) -> None:
    turmas_por_turno = list(filter(lambda t: t.turno == turno.id, turmas))
    turnos_dias = list(map(lambda dia: __get_turno_dia__(dia, turmas_por_turno), dias_da_semana))
    turno.dias_da_semana = turnos_dias


def __get_turno_dia__(dia_da_semana: str, turmas: List[Turma]) -> TurnoDia:
    turno_dia = TurnoDia()
    turno_dia.id = dia_da_semana
    turno_dia.aulas = []
    [__set_aula__(turma, turno_dia) for turma in turmas]

    return turno_dia


def __set_aula__(turma: Turma, turno_dia: TurnoDia) -> None:
    aula = Aula()
    aula.turma = turma.id
    turno_dia.aulas.append(aula)
