from professor.function.get_professores import get_professores
from turma.function.get_todas_as_turmas import get_todas_as_turmas


def perform_organizacao() -> dict:
    turmas = get_todas_as_turmas()
    professores = get_professores()

    return {
        'turmas': [
            {
                'id': '191',
                'periodos': [
                    {'mat': 5},
                    {'port': 5},
                ]
            },
            {'id': '192'}
        ]
    }
