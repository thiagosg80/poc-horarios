from professor.function.get_professores import get_professores
from turma.function.get_todas_as_turmas import get_todas_as_turmas
from turma.function.get_turnos_grade import get_turnos_grade
from turma.model.grade.turma import GradeTurma
from turma.model.grade.dia import GradeDia
from turma.model.grade.turno import GradeTurno


def perform_organizacao() -> dict:
    turmas = get_todas_as_turmas()
    turnos_grade = get_turnos_grade(turmas)
    professores = get_professores()

    return {
        'turnos': list(map(__get_turnos__, turnos_grade))
    }


def __get_turnos__(turno: GradeTurno) -> dict:

    return {
        'id': turno.id,
        'dias_da_semana': list(map(__get_dias_da_semana__, turno.dias_da_semana))
    }


def __get_dias_da_semana__(dia_da_semana: GradeDia) -> dict:
    return {
        'id': dia_da_semana.id,
        'turmas': list(map(__get_grade_turmas__, dia_da_semana.grade_turmas))
    }


def __get_grade_turmas__(grade_turma: GradeTurma) -> dict:
    return {
        'id': grade_turma.id,
        'periodo_1': grade_turma.periodo_1,
        'periodo_2': grade_turma.periodo_2,
        'periodo_3': grade_turma.periodo_3,
        'periodo_4': grade_turma.periodo_4,
        'periodo_5': grade_turma.periodo_5
    }
