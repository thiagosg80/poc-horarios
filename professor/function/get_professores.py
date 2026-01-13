from professor.model.aula import Aula
from professor.model.disponibilidade import Disponibilidade
from professor.model.professor import Professor


def get_professores(turmas_map: dict) -> list[Professor]:
    return [
        # __get_professor('andreia p', 'port', __get_turmas_01(), turmas_map, __get_disponibilidades_01(), 1),
        # __get_professor('josiane', 'mat', __get_turmas_02(), turmas_map, __get_disponibilidades_02(), 1),
        # __get_professor('patricia', 'mat', __get_turmas_03(), turmas_map, __get_disponibilidades_03(), 1),
        # __get_professor('cristian', 'geo', __get_turmas_04(), turmas_map, __get_disponibilidades_04(), 1),
        # __get_professor('jeferson', 'ingl', __get_turmas_04(), turmas_map, __get_disponibilidades_05(), 1),
        __get_professor('robson', 'ef', __get_turmas_04(), turmas_map, __get_disponibilidades_06(), 2),
        # __get_professor('edson', 'hist', __get_turmas_04(), turmas_map, __get_disponibilidades_07(), 1),
        # __get_professor('crissiane', 'ic', __get_turmas_04(), turmas_map, __get_disponibilidades_08(), 1),
        # __get_professor('maristela', 'cie', __get_turmas_04(), turmas_map, __get_disponibilidades_09(), 1),
        # __get_professor('elaine', 'art', __get_turmas_04(), turmas_map, __get_disponibilidades_10(), 1),
        # __get_professor('lilian', 'er', __get_turmas_05(), turmas_map, __get_disponibilidades_11(), 1),
        # __get_professor('andrelise', 'er', __get_turmas_06(), turmas_map, __get_disponibilidades_12(), 1),
        # __get_professor('cristian', 'er', __get_turmas_07(), turmas_map, __get_disponibilidades_13(), 1),
        # __get_professor('lilian mat', 'mat', __get_turmas_08(), turmas_map, __get_disponibilidades_14(), 1),
        # __get_professor('andreia s', 'port', __get_turmas_09(), turmas_map, __get_disponibilidades_15(), 1),

        # __get_professor('natasha', 'port', __get_turmas_10(), turmas_map, __get_disponibilidades_16(), 1)
    ]

def __get_professor(nome: str, disciplina: str, turmas: list[str], turmas_map: dict,
                    disponibilidades: list[Disponibilidade],
                    quantidade_minima_periodos_consecutivos: int) -> Professor:

    professor = Professor()
    professor.nome = nome
    professor.disciplina = disciplina
    professor.aulas = __get_aulas(turmas, disciplina, turmas_map, quantidade_minima_periodos_consecutivos)
    professor.disponibilidades = disponibilidades

    return professor

def __get_aulas(turmas: list[str], disciplina: str, turmas_map: dict,
                quantidade_minima_periodos_consecutivos: int) -> list[Aula]:

    return list(map(lambda i: __get_aula(i, disciplina, turmas_map, quantidade_minima_periodos_consecutivos), turmas))

def __get_aula(turma: str, disciplina: str, turmas_map: dict, quantidade_minima_periodos_consecutivos: int) -> Aula:
    aula = Aula()
    aula.turma = turma
    aula.disciplina = disciplina
    quantidade_periodos = turmas_map.get(turma).disciplina_map.get(disciplina).quantidade_periodos
    aula.quantidade_maxima_periodos_consecutivos = int(quantidade_periodos / 2) + 1
    aula.quantidade_minima_periodos_consecutivos = quantidade_minima_periodos_consecutivos

    return aula

def __get_turmas_01() -> list[str]:
    return [
        '161', '162', '171', '172', '181'
    ]

def __get_turmas_02() -> list[str]:
    return [
        '161', '162'
    ]

def __get_turmas_03() -> list[str]:
    return [
        '172', '181', '182'
    ]

def __get_turmas_04() -> list[str]:
    return [
        '161', '162', '171', '172', '181', '182', '191', '192'
    ]

def __get_turmas_05() -> list[str]:
    return [
        '162', '172'
    ]

def __get_turmas_06() -> list[str]:
    return [
        '182', '192'
    ]

def __get_turmas_07() -> list[str]:
    return [
        '161', '171', '181', '191'
    ]

def __get_turmas_08() -> list[str]:
    return [
        '171', '191', '192'
    ]

def __get_turmas_09() -> list[str]:
    return [
        '182', '191', '192'
    ]

def __get_turmas_10() -> list[str]:
    return [
        '182', '192', '183'
    ]

def __get_disponibilidades_01() -> list[Disponibilidade]:
    return [
        __get_disponibilidade('seg', 'manha', 5),
        __get_disponibilidade('qua', 'manha', 5),
        __get_disponibilidade('sex', 'manha', 5),
        __get_disponibilidade('seg', 'tarde', 4),
        __get_disponibilidade('qua', 'tarde', 1),
        __get_disponibilidade('sex', 'tarde', 5)
    ]

def __get_disponibilidades_02() -> list[Disponibilidade]:
    return [
        __get_disponibilidade('ter', 'manha', 2),
        __get_disponibilidade('qua', 'manha', 2),
        __get_disponibilidade('qui', 'manha', 1),
        __get_disponibilidade('ter', 'tarde', 2),
        __get_disponibilidade('qua', 'tarde', 2),
        __get_disponibilidade('qui', 'tarde', 1)
    ]

def __get_disponibilidades_03() -> list[Disponibilidade]:
    return [
        __get_disponibilidade('seg', 'manha', 2),
        __get_disponibilidade('qua', 'manha', 3),
        __get_disponibilidade('seg', 'tarde', 5),
        __get_disponibilidade('qua', 'tarde', 5)
    ]

def __get_disponibilidades_04() -> list[Disponibilidade]:
    return [
        __get_disponibilidade('seg', 'manha', 4),
        __get_disponibilidade('qua', 'manha', 4),
        __get_disponibilidade('seg', 'tarde', 3),
        __get_disponibilidade('qua', 'tarde', 5)
    ]

def __get_disponibilidades_05() -> list[Disponibilidade]:
    return [
        __get_disponibilidade('seg', 'manha', 3),
        __get_disponibilidade('qui', 'manha', 5),
        __get_disponibilidade('seg', 'tarde', 3),
        __get_disponibilidade('qui', 'tarde', 5)
    ]

def __get_disponibilidades_06() -> list[Disponibilidade]:
    return [
        __get_disponibilidade('seg', 'manha', 4),
        __get_disponibilidade('qua', 'manha', 1),
        __get_disponibilidade('sex', 'manha', 3),
        __get_disponibilidade('qua', 'tarde', 2),
        __get_disponibilidade('qui', 'tarde', 1),
        __get_disponibilidade('sex', 'tarde', 5)
    ]

def __get_disponibilidades_07() -> list[Disponibilidade]:
    return [
        __get_disponibilidade('ter', 'manha', 4),
        __get_disponibilidade('qui', 'manha', 4),
        __get_disponibilidade('ter', 'tarde', 4),
        __get_disponibilidade('qui', 'tarde', 4)
    ]

def __get_disponibilidades_08() -> list[Disponibilidade]:
    return [
        __get_disponibilidade('ter', 'manha', 3),
        __get_disponibilidade('sex', 'manha', 5),
        __get_disponibilidade('ter', 'tarde', 3),
        __get_disponibilidade('sex', 'tarde', 5)
    ]

def __get_disponibilidades_09() -> list[Disponibilidade]:
    return [
        __get_disponibilidade('ter', 'manha', 3),
        __get_disponibilidade('qua', 'manha', 5),
        __get_disponibilidade('ter', 'tarde', 4),
        __get_disponibilidade('qua', 'tarde', 4)
    ]

def __get_disponibilidades_10() -> list[Disponibilidade]:
    return [
        __get_disponibilidade('ter', 'manha', 3),
        __get_disponibilidade('qui', 'manha', 5),
        __get_disponibilidade('ter', 'tarde', 3),
        __get_disponibilidade('qui', 'tarde', 5)
    ]

def __get_disponibilidades_11() -> list[Disponibilidade]:
    return [
        __get_disponibilidade('qui', 'tarde', 2)
    ]

def __get_disponibilidades_12() -> list[Disponibilidade]:
    return [
        __get_disponibilidade('qua', 'tarde', 1),
        __get_disponibilidade('qui', 'tarde', 1)
    ]

def __get_disponibilidades_13() -> list[Disponibilidade]:
    return [
        __get_disponibilidade('seg', 'manha', 1),
        __get_disponibilidade('sex', 'manha', 3)
    ]

def __get_disponibilidades_14() -> list[Disponibilidade]:
    return [
        __get_disponibilidade('ter', 'manha', 5),
        __get_disponibilidade('qui', 'manha', 5),
        __get_disponibilidade('ter', 'tarde', 4),
        __get_disponibilidade('qui', 'tarde', 1)
    ]

def __get_disponibilidades_15() -> list[Disponibilidade]:
    return [
        __get_disponibilidade('seg', 'manha', 1),
        __get_disponibilidade('sex', 'manha', 4),
        __get_disponibilidade('seg', 'tarde', 5),
        __get_disponibilidade('sex', 'tarde', 5)
    ]

def __get_disponibilidades_16() -> list[Disponibilidade]:
    return [
        __get_disponibilidade('seg', 'tarde', 5),
        __get_disponibilidade('ter', 'tarde', 5),
        __get_disponibilidade('qui', 'tarde', 5),
        __get_disponibilidade('sex', 'tarde', 5)
    ]

def __get_disponibilidade(dia_da_semana: str, turno: str, quantidade_de_periodos: int) -> Disponibilidade:
    disponibilidade = Disponibilidade()
    disponibilidade.dia = dia_da_semana
    disponibilidade.turno = turno
    disponibilidade.quantidade_de_periodos = quantidade_de_periodos

    return disponibilidade
