import random
from random import randrange
from typing import List

from professor.model.disponibilidade import Disponibilidade
from professor.model.professor import Professor
from turma.model.grade.periodo import Periodo


def set_organizacao(professores: List[Professor], periodos: List[Periodo], turmas_map: dict) -> None:
    disponibilidades: List[dict] = []
    for professor in professores:
        __add_disponibilidades__(professor, disponibilidades)

    while len(list(filter(lambda i: not i.get('is_busy'), disponibilidades))) > 0:
        __inicializar__(periodos, disponibilidades)

        for periodo in periodos:
            possibilidades = __get_possibilidades__(periodo, disponibilidades, turmas_map)
            __set_alocacao__(periodo, possibilidades, turmas_map, periodos)


def __add_disponibilidades__(professor: Professor, disponibilidades: List[dict]) -> None:
    for d in professor.disponibilidades:
        for q in range(d.quantidade_de_periodos):
            disponibilidades.append(__get_disponibilidade__(d, professor))


def __get_disponibilidade__(disponibilidade_input: Disponibilidade, professor: Professor) -> dict:
    aula = professor.aulas[0]

    return {
        'nome': professor.nome,
        'dia': disponibilidade_input.dia,
        'turno': disponibilidade_input.turno,
        'turmas_ids': list(map(lambda i: i.turma, professor.aulas)),
        'disciplina': aula.disciplina,
        'quantidade_maxima_periodos_consecutivos': aula.quantidade_maxima_periodos_consecutivos,
        'is_busy': False
    }


def __inicializar__(periodos: List[Periodo], disponibilidades: List[dict]) -> None:
    for periodo in periodos:
        periodo.descricao = ''

    random.shuffle(periodos)

    for disponibilidade in disponibilidades:
        disponibilidade['is_busy'] = False


def __get_possibilidades__(periodo: Periodo, disponibilidades: List[dict], turmas_map: dict) -> List[dict]:
    return list(filter(lambda i: __is_match_disponibilidade__(i, periodo, turmas_map), disponibilidades))


def __is_match_disponibilidade__(d: dict, periodo: Periodo, turmas_map: dict) -> bool:
    turma = turmas_map.get(periodo.turma)
    is_turma_ok = periodo.turma in d['turmas_ids']

    return d['dia'] == periodo.dia and is_turma_ok and d['turno'] == turma.turno and not d['is_busy']


def __set_alocacao__(periodo: Periodo, possibilidades: List[dict], turmas_map: dict, periodos: List[Periodo]) -> None:
    size = len(possibilidades)
    if size > 0:
        index = randrange(size)
        possibilidade = possibilidades[index]
        periodo_descricao = possibilidade['disciplina'] + ' - ' + possibilidade['nome']
        if __is_suitable__(periodo, turmas_map, periodos, periodo_descricao, possibilidade):
            periodo.descricao = periodo_descricao
            possibilidade['is_busy'] = True


def __is_suitable__(periodo: Periodo, turmas_map: dict, periodos: List[Periodo], periodo_descricao: str,
                    possibilidade: dict) -> bool:

    turma_id = periodo.turma
    disciplina = possibilidade.get('disciplina')
    quantidade_periodos = turmas_map.get(turma_id).disciplina_map.get(disciplina).quantidade_periodos
    periodos_preenchidos = list(filter(lambda i: i.descricao == periodo_descricao and i.turma == turma_id, periodos))
    periodos_diarios_preenchidos = list(filter(lambda i: i.dia == periodo.dia, periodos_preenchidos))
    quantidade_maxima_periodos_consecutivos = possibilidade.get('quantidade_maxima_periodos_consecutivos')

    nao_ha_periodos_na_mesma_ordem_no_mesmo_dia = __nao_ha_periodos_na_mesma_ordem_no_mesmo_dia__(
        periodo, periodos, periodo_descricao, turmas_map)

    return (quantidade_periodos > len(periodos_preenchidos) and quantidade_maxima_periodos_consecutivos >
            len(periodos_diarios_preenchidos) and nao_ha_periodos_na_mesma_ordem_no_mesmo_dia)


def __nao_ha_periodos_na_mesma_ordem_no_mesmo_dia__(periodo: Periodo, periodos: List[Periodo],
                                                    periodo_descricao: str, turmas_map: dict) -> bool:

    filtered = list(filter(lambda i: __mesmo_dia_e_ordem_callback__(i, periodo, periodo_descricao, turmas_map),
                           periodos))

    return len(filtered) == 0


def __mesmo_dia_e_ordem_callback__(i: Periodo, periodo: Periodo, periodo_descricao: str, turmas_map: dict) -> bool:
    is_mesmo_turno = turmas_map.get(i.turma).turno == turmas_map.get(periodo.turma).turno

    return i.dia == periodo.dia and i.ordem == periodo.ordem and i.descricao == periodo_descricao and is_mesmo_turno

