from typing import List

from professor.model.aula import Aula
from professor.model.disponibilidade import Disponibilidade
from professor.model.professor import Professor


def get_professores(turmas_map: dict) -> List[Professor]:
    return [
        __get_professor__('andreia p', 'port', __get_turmas_01__(), turmas_map, __get_disponibilidades_01__()),
        # __get_professor__('josiane', 'mat', __get_turmas_02__(), __get_disponibilidades_02__()),
        # __get_professor__('patricia', 'mat', __get_turmas_03__(), __get_disponibilidades_03__()),
        # __get_professor__('cristian', 'geo', __get_turmas_04__(), __get_disponibilidades_04__()),
        # __get_professor__('jeferson', 'ingl', __get_turmas_04__(), __get_disponibilidades_05__()),
        # __get_professor__('robson', 'ef', __get_turmas_04__(), __get_disponibilidades_06__())
    ]


def __get_professor__(nome: str, disciplina: str, turmas: List[str], turmas_map: dict,
                      disponibilidades: List[Disponibilidade]) -> Professor:

    professor = Professor()
    professor.nome = nome
    professor.disciplina = disciplina
    professor.aulas = __get_aulas__(turmas, disciplina, turmas_map)
    professor.disponibilidades = disponibilidades

    return professor


def __get_aulas__(turmas: List[str], disciplina: str, turmas_map: dict) -> List[Aula]:
    return list(map(lambda i: __get_aula__(i, disciplina, turmas_map), turmas))


def __get_aula__(turma: str, disciplina: str, turmas_map: dict) -> Aula:
    aula = Aula()
    aula.turma = turma
    aula.disciplina = disciplina
    quantidade_periodos = turmas_map.get(turma).disciplina_map.get(disciplina).quantidade_periodos
    aula.quantidade_maxima_periodos_consecutivos = int(quantidade_periodos / 2) + 1

    return aula


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
