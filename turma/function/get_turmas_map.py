from typing import List

from turma.model.disciplina import Disciplina
from turma.model.turma import Turma


def get_turmas_map() -> dict:
    return {
        '161': __get_turma__('manha', __get_disciplina_map_default__()),
        '162': __get_turma__('tarde', __get_disciplina_map_default__()),
        '171': __get_turma__('manha', __get_disciplina_map_default__()),
        '172': __get_turma__('tarde', __get_disciplina_map_default__()),
        '181': __get_turma__('manha', __get_disciplina_map_default__()),
        '182': __get_turma__('tarde', __get_disciplina_map_default__()),
        '191': __get_turma__('manha', __get_disciplina_map_default__()),
        '192': __get_turma__('tarde', __get_disciplina_map_default__())
    }


def __get_turma__(turno: str, disciplinas: dict) -> Turma:
    turma = Turma()
    turma.turno = turno
    turma.disciplina_map = disciplinas

    return turma


def __get_disciplina_map_default__() -> dict:
    return {
        'mat': __get_disciplina__(5),
        'port': __get_disciplina__(5),
        'geo': __get_disciplina__(2),
        'hist': __get_disciplina__(2),
        'ingl': __get_disciplina__(2),
        'ic': __get_disciplina__(2),
        'cie': __get_disciplina__(2),
        'art': __get_disciplina__(2),
        'er': __get_disciplina__(1),
        'ef': __get_disciplina__(2)
    }


def __get_disciplina__(quantidade_periodos: int) -> Disciplina:
    disciplina = Disciplina()
    disciplina.quantidade_periodos = quantidade_periodos

    return disciplina
