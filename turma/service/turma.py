from typing import List

from turma.model.disciplina import Disciplina
from turma.model.turma import Turma


class TurmaService:
    def get_todas(self) -> List[Turma]:
        return [
            self.__get_turma__('161', self.__get_disciplinas_default()),
            self.__get_turma__('162', self.__get_disciplinas_default()),
            self.__get_turma__('171', self.__get_disciplinas_default()),
            self.__get_turma__('172', self.__get_disciplinas_default()),
            self.__get_turma__('181', self.__get_disciplinas_default()),
            self.__get_turma__('182', self.__get_disciplinas_default()),
            self.__get_turma__('191', self.__get_disciplinas_default()),
            self.__get_turma__('192', self.__get_disciplinas_default())
        ]

    def __get_turma__(self, id: str, disciplinas: List[Disciplina]) -> Turma:
        turma = Turma()
        turma.id = id
        turma.disciplinas = disciplinas

        return turma

    def __get_disciplinas_default(self) -> List[Disciplina]:
        return [
            self.__get_disciplina__('mat', 5),
            self.__get_disciplina__('port', 5),
            self.__get_disciplina__('geo', 2),
            self.__get_disciplina__('hist', 2),
            self.__get_disciplina__('ingl', 2),
            self.__get_disciplina__('ic', 2),
            self.__get_disciplina__('cie', 2),
            self.__get_disciplina__('art', 2),
            self.__get_disciplina__('er', 1),
            self.__get_disciplina__('ef', 2)
        ]

    def __get_disciplina__(self, id: str, quantidade_periodos: int) -> Disciplina:
        disciplina = Disciplina()
        disciplina.id = id
        disciplina.quantidade_periodos = quantidade_periodos

        return disciplina
