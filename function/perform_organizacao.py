from typing import List

from flask import Response

from function.get_dias_da_semana import get_dias_da_semana
from professor.function.get_professores import get_professores
from turma.function.get_periodos import get_periodos
from turma.function.get_turmas_map import get_turmas_map
from turma.function.get_turnos_grade import get_turnos_grade
from turma.function.grade.get_grade_file import get_grade_file
from function.set_organizacao import set_organizacao
from turma.model.grade.periodo import Periodo
from turma.model.grade.turma import GradeTurma
from turma.model.grade.dia import GradeDia
from turma.model.grade.turno import GradeTurno


def perform_organizacao() -> Response:
    turmas_map = get_turmas_map()
    dias_da_semana = get_dias_da_semana()
    periodos = get_periodos(list(map(lambda key: key, turmas_map)), dias_da_semana)
    turnos_grade = get_turnos_grade(turmas_map, dias_da_semana, periodos)
    professores = get_professores(turmas_map)
    set_organizacao(professores, turmas_map, turnos_grade)

    grade = {
        'turnos': list(map(lambda i: __get_turnos__(i, periodos), turnos_grade))
    }

    return get_grade_file(grade)


def __get_turnos__(turno: GradeTurno, periodos: List[Periodo]) -> dict:
    return {
        'id': turno.id,
        'dias_da_semana': list(map(lambda i: __get_dias_da_semana__(i, periodos), turno.dias_da_semana))
    }


def __get_dias_da_semana__(dia_da_semana: GradeDia, periodos: List[Periodo]) -> dict:
    periodos_by_dia = list(filter(lambda i: i.dia == dia_da_semana.id, periodos))

    return {
        'id': dia_da_semana.id,
        'turmas': list(map(lambda i: __get_grade_turmas__(i, periodos_by_dia), dia_da_semana.grade_turmas))
    }


def __get_grade_turmas__(grade_turma: GradeTurma, periodos_input: List[Periodo]) -> dict:
    periodos_filtered = list(filter(lambda i: i.turma == grade_turma.id, periodos_input))
    periodos = sorted(periodos_filtered, key=lambda i: i.ordem)

    return {
        'id': grade_turma.id,
        'periodos': list(map(__get_periodo__, periodos))
    }


def __get_periodo__(periodo: Periodo) -> dict:
    return {
        'ordem': periodo.ordem,
        'descricao': periodo.descricao
    }
