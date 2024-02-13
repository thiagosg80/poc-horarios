from typing import List

from professor.model.disponibilidade import Disponibilidade
from professor.model.professor import Professor


def get_professores() -> List[Professor]:
    return [
        __get_professor__('andreia p', 'port', __get_turmas_01__(), __get_disponibilidades_01__()),
        __get_professor__('josiane', 'mat', __get_turmas_02__(), __get_disponibilidades_02__())
    ]


def __get_professor__(nome: str, disciplina: str, turmas: List[str], disponibilidades: List[Disponibilidade]) \
        -> Professor:

    professor = Professor()
    professor.nome = nome
    professor.disciplina = disciplina
    professor.turmas = turmas
    professor.disponibilidades = disponibilidades

    return professor


def __get_turmas_01__() -> List[str]:
    return [
        '161', '162', '171', '172', '181'
    ]


def __get_turmas_02__() -> List[str]:
    return [
        '161', '162'
    ]


def __get_disponibilidades_01__() -> List[Disponibilidade]:
    return [
        __get_disponibilidade__('seg', 'manha', 5),
        __get_disponibilidade__('qua', 'manha', 5),
        __get_disponibilidade__('sex', 'manha', 5),
        __get_disponibilidade__('seg', 'tarde', 4),
        __get_disponibilidade__('qua', 'tarde', 1),
        __get_disponibilidade__('sex', 'tarde', 5)
    ]


def __get_disponibilidades_02__() -> List[Disponibilidade]:
    return [
        __get_disponibilidade__('ter', 'manha', 2),
        __get_disponibilidade__('qua', 'manha', 2),
        __get_disponibilidade__('qui', 'manha', 1),
        __get_disponibilidade__('ter', 'tarde', 2),
        __get_disponibilidade__('qua', 'tarde', 2),
        __get_disponibilidade__('qui', 'tarde', 1)
    ]


def __get_disponibilidade__(dia_da_semana: str, turno: str, quantidade_de_periodos: int) -> Disponibilidade:
    disponibilidade = Disponibilidade()
    disponibilidade.dia_semana = dia_da_semana
    disponibilidade.turno = turno
    disponibilidade.quantidade_de_periodos = quantidade_de_periodos

    return disponibilidade
