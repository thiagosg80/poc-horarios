from typing import List

from turma.model.disciplina import Disciplina
from turma.model.turma import Turma


def get_todas_as_turmas() -> List[Turma]:
    return [
        __get_turma__('161', 'manha', __get_disciplinas_default__()),
        __get_turma__('162', 'tarde', __get_disciplinas_default__()),
        __get_turma__('171', 'manha', __get_disciplinas_default__()),
        __get_turma__('172', 'tarde', __get_disciplinas_default__()),
        __get_turma__('181', 'manha', __get_disciplinas_default__()),
        __get_turma__('182', 'tarde', __get_disciplinas_default__()),
        __get_turma__('191', 'manha', __get_disciplinas_default__()),
        __get_turma__('192', 'tarde', __get_disciplinas_default__())
    ]


def __get_turma__(id: str, turno: str, disciplinas: List[Disciplina]) -> Turma:
    turma = Turma()
    turma.id = id
    turma.turno = turno
    turma.disciplinas = disciplinas

    return turma


def __get_disciplinas_default__() -> List[Disciplina]:
    return [
        __get_disciplina__('mat', 5),
        __get_disciplina__('port', 5),
        __get_disciplina__('geo', 2),
        __get_disciplina__('hist', 2),
        __get_disciplina__('ingl', 2),
        __get_disciplina__('ic', 2),
        __get_disciplina__('cie', 2),
        __get_disciplina__('art', 2),
        __get_disciplina__('er', 1),
        __get_disciplina__('ef', 2)
    ]


def __get_disciplina__(id: str, quantidade_periodos: int) -> Disciplina:
    disciplina = Disciplina()
    disciplina.id = id
    disciplina.quantidade_periodos = quantidade_periodos

    return disciplina
