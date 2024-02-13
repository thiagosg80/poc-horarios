from professor.service.professor import get_professores
from turma.service.turma import get_todas_as_turmas


class OrganizacaoService:
    def perform(self) -> dict:
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
