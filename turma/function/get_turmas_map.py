from typing import List

from turma.model.disciplina import Disciplina
from turma.model.turma import Turma


def get_turmas_map() -> dict:
    return {
        '161': __get_turma('manha', __get_disciplina_map_default()),
        '162': __get_turma('tarde', __get_disciplina_map_default()),
        '171': __get_turma('manha', __get_disciplina_map_default()),
        '172': __get_turma('tarde', __get_disciplina_map_default()),
        '181': __get_turma('manha', __get_disciplina_map_default()),
        '182': __get_turma('tarde', __get_disciplina_map_default()),
        '191': __get_turma('manha', __get_disciplina_map_default()),
        '192': __get_turma('tarde', __get_disciplina_map_default())
    }


def __get_turma(turno: str, disciplinas: dict) -> Turma:
    turma = Turma()
    turma.turno = turno
    turma.disciplina_map = disciplinas

    return turma


def __get_disciplina_map_default() -> dict:
    return {
        'mat': __get_disciplina(5),
        'port': __get_disciplina(5),
        'geo': __get_disciplina(2),
        'hist': __get_disciplina(2),
        'ingl': __get_disciplina(2),
        'ic': __get_disciplina(2),
        'cie': __get_disciplina(2),
        'art': __get_disciplina(2),
        'er': __get_disciplina(1),
        'ef': __get_disciplina(2)
    }


def __get_disciplina(quantidade_periodos: int) -> Disciplina:
    disciplina = Disciplina()
    disciplina.quantidade_periodos = quantidade_periodos

    return disciplina
