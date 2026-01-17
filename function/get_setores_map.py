from itertools import chain, combinations
from typing import List

from function.get_empty_sector import get_empty_sector
from model.sector import Sector
from professor.model.disponibilidade import Disponibilidade
from professor.model.professor import Professor
from turma.function.get_periodos_ordens import get_periodos_ordens


def get_setores_map(professores: List[Professor]) -> dict:
    quantidade_maxima_disponibilidade: int = __get_quantidade_maxima_disponibilidade(professores)
    limit: range = range(1, quantidade_maxima_disponibilidade + 1)

    return {d: __get_setores_by_disponibilidade(d, get_periodos_ordens()) for d in limit}


def __get_quantidade_maxima_disponibilidade(professores: List[Professor]) -> int:
    disponibilidades_raw: List = list(map(lambda i: i.disponibilidades, professores))
    disponibilidades: List[Disponibilidade] = list(chain.from_iterable(disponibilidades_raw))
    quantidades_de_periodos: List[int] = list(map(lambda i: i.quantidade_de_periodos, disponibilidades))

    return max(quantidades_de_periodos)


def __get_setores_by_disponibilidade(quantidade_disponivel: int, periodos_ordens: List[int]) -> List[Sector]:
    combinacoes: List[tuple] = list(combinations(periodos_ordens, quantidade_disponivel))
    sector: Sector = get_empty_sector(periodos_ordens)

    return [{}]