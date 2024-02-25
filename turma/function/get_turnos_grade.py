from typing import List

from turma.model.grade.periodo import Periodo
from turma.model.grade.turma import GradeTurma
from turma.model.grade.dia import GradeDia
from turma.model.grade.turno import GradeTurno
from turma.model.turma import Turma


def get_turnos_grade(turmas_map: dict, dias_da_semana: List[str], periodos: List[Periodo]) -> List[GradeTurno]:
    turnos_set = list(set(map(lambda t: t[1].turno, turmas_map.items())))
    turnos = list(map(__turno_callback__, turnos_set))
    [__set_turnos__(turno, turmas_map, dias_da_semana, periodos) for turno in turnos]

    return turnos


def __turno_callback__(turno: str) -> GradeTurno:
    grade_turno = GradeTurno()
    grade_turno.id = turno

    return grade_turno


def __set_turnos__(turno: GradeTurno, turmas_map: dict, dias_da_semana: List[str], periodos: List[Periodo]) -> None:
    turmas_por_turno_map = dict(filter(lambda t: t[1].turno == turno.id, turmas_map.items()))
    turnos_dias = list(map(lambda dia: __get_grade_dia__(dia, turmas_por_turno_map, periodos), dias_da_semana))
    turno.dias_da_semana = turnos_dias


def __get_grade_dia__(dia_da_semana: str, turmas_map: dict, periodos: List[Periodo]) -> GradeDia:
    grade_dia = GradeDia()
    grade_dia.id = dia_da_semana
    grade_dia.grade_turmas = []
    [__set_turma__(key, grade_dia, periodos) for key in turmas_map]

    return grade_dia


def __set_turma__(turma_id: str, grade_dia: GradeDia, periodos: List[Periodo]) -> None:
    grade_turma = GradeTurma()
    grade_turma.id = turma_id
    grade_turma.periodos = periodos
    grade_dia.grade_turmas.append(grade_turma)
