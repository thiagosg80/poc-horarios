from professor.function.get_professores import get_professores
from turma.function.get_todas_as_turmas import get_todas_as_turmas
from turma.function.get_turmas_grade import get_turmas_grade
from turma.model.grade.aula import Aula
from turma.model.grade.dia import TurnoDia
from turma.model.grade.turno import GradeTurno


def perform_organizacao() -> dict:
    turmas = get_todas_as_turmas()
    turmas_grade = get_turmas_grade(turmas)
    professores = get_professores()

    return {
        'turnos': list(map(__get_turnos__, turmas_grade.turnos))
    }


def __get_turnos__(turno: GradeTurno) -> dict:

    return {
        'id': turno.id,
        'dias_da_semana': list(map(__get_dias_da_semana__, turno.dias_da_semana))
    }


def __get_dias_da_semana__(dia_da_semana: TurnoDia) -> dict:
    return {
        'id': dia_da_semana.id,
        'aulas': list(map(__get_aulas__, dia_da_semana.aulas))
    }


def __get_aulas__(aula: Aula) -> dict:
    return {
        'turma': aula.turma,
        'periodo_1': aula.periodo_1,
        'periodo_2': aula.periodo_2,
        'periodo_3': aula.periodo_3,
        'periodo_4': aula.periodo_4,
        'periodo_5': aula.periodo_5
    }
