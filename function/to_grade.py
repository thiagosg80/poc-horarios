from typing import List

from turma.model.grade.dia import GradeDia
from turma.model.grade.periodo import Periodo
from turma.model.grade.turma import GradeTurma
from turma.model.grade.turno import GradeTurno


def to_grade(turnos_grade: List[GradeTurno], periodos: List[Periodo]) -> dict:
    return {
        'turnos': list(map(lambda i: __get_turnos(i, periodos), turnos_grade))
    }


def __get_turnos(turno: GradeTurno, periodos: List[Periodo]) -> dict:
    return {
        'id': turno.id,
        'dias_da_semana': list(map(lambda i: __get_dias_da_semana(i, periodos), turno.dias_da_semana))
    }


def __get_dias_da_semana(dia_da_semana: GradeDia, periodos: List[Periodo]) -> dict:
    periodos_by_dia = list(filter(lambda i: i.dia == dia_da_semana.id, periodos))

    return {
        'id': dia_da_semana.id,
        'turmas': list(map(lambda i: __get_grade_turmas(i, periodos_by_dia), dia_da_semana.grade_turmas))
    }


def __get_grade_turmas(grade_turma: GradeTurma, periodos_input: List[Periodo]) -> dict:
    periodos_filtered = list(filter(lambda i: i.dia == periodos_input[0].dia, grade_turma.periodos))
    ordered = sorted(periodos_filtered, key=lambda i: i.ordem)
    periodos = list(map(__get_periodo, ordered))

    return {
        'id': grade_turma.id,
        'periodos': periodos
    }


def __get_periodo(periodo: Periodo) -> dict:
    return {
        'ordem': periodo.ordem,
        'descricao': periodo.descricao
    }