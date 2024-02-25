from typing import List

from turma.model.disciplina import Disciplina
from turma.model.turma import Turma


def get_turmas_map() -> dict:
    return {
        '161': __get_turma__('manha', __get_disciplinas_default__()),
        '162': __get_turma__('tarde', __get_disciplinas_default__()),
        '171': __get_turma__('manha', __get_disciplinas_default__()),
        '172': __get_turma__('tarde', __get_disciplinas_default__()),
        '181': __get_turma__('manha', __get_disciplinas_default__()),
        '182': __get_turma__('tarde', __get_disciplinas_default__()),
        '191': __get_turma__('manha', __get_disciplinas_default__()),
        '192': __get_turma__('tarde', __get_disciplinas_default__())
    }


def __get_turma__(turno: str, disciplinas: List[Disciplina]) -> Turma:
    turma = Turma()
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
