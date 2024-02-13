from professor.function.get_professores import get_professores
from turma.function.get_todas_as_turmas import get_todas_as_turmas
from turma.function.get_turmas_grade import get_turmas_grade


def perform_organizacao() -> dict:
    turmas = get_todas_as_turmas()
    turmas_grade = get_turmas_grade(turmas)
    professores = get_professores()

    return {
        'turnos': {}
    }
