from turma.service.turma import TurmaService


class OrganizacaoService:
    def perform(self) -> dict:
        turmas = TurmaService().get_todas()

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
