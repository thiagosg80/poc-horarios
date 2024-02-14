from typing import List

from professor.model.disponibilidade import Disponibilidade
from professor.model.professor import Professor
from turma.model.grade.periodo import Periodo
from turma.model.turma import Turma


def set_organizacao(professor: Professor, periodos: List[Periodo], turmas: List[Turma]) -> None:
    dias_disponiveis = list(map(lambda i: i.dia, professor.disponibilidades))
    periodos_filtrados = list(filter(lambda i: i.dia in dias_disponiveis and i.turma in professor.turmas, periodos))
    periodos_ja_alocados = []
    for periodo in periodos_filtrados:
        turma = list(filter(lambda i: i.id == periodo.turma, turmas))[0]
        disciplina = list(filter(lambda i: i.id == professor.disciplina, turma.disciplinas))[0]

        disponibilidade = __get_disponibilidade__(professor, turma.turno, periodo.dia) \
            if disciplina.quantidade_periodos > 0 else __get_empty_disponibilidade__()

        periodo_descricao = professor.disciplina + ' - ' + professor.nome

        if (disponibilidade.quantidade_de_periodos > 0 and __nao_tem_marcacoes_consecutivas_ainda__(
                3, periodos_filtrados, turma.id, periodo.dia, periodo_descricao) and disciplina.quantidade_periodos > 0
                and not periodo.descricao and __nao_ha_periodos_simultaneos__(periodos_ja_alocados, periodo, turmas)):

            periodo.descricao = periodo_descricao
            disponibilidade.quantidade_de_periodos -= 1
            disciplina.quantidade_periodos -= 1
            periodos_ja_alocados.append(periodo)


def __get_disponibilidade__(professor: Professor, turno: str, dia: str) -> Disponibilidade:
    disponibilidades = list(filter(lambda i: i.turno == turno and i.dia == dia, professor.disponibilidades))

    return disponibilidades[0] if len(disponibilidades) > 0 else __get_empty_disponibilidade__()


def __get_empty_disponibilidade__() -> Disponibilidade:
    disponibilidade = Disponibilidade()
    disponibilidade.quantidade_de_periodos = 0

    return disponibilidade


def __nao_tem_marcacoes_consecutivas_ainda__(quantidade: int, periodos: List[Periodo], turma_id: str, dia_id: str,
                                             periodo_descricao: str) -> bool:
    periodos_filtrados = list(filter(
        lambda i: i.dia == dia_id and i.turma == turma_id and i.descricao == periodo_descricao, periodos))

    return len(periodos_filtrados) < quantidade


def __nao_ha_periodos_simultaneos__(periodos_ja_alocados: List[Periodo], periodo: Periodo,
                                    turmas: List[Turma]) -> bool:

    simultaneos = list(filter(lambda i: __is_simultaneos_callback__(i, periodo, turmas), periodos_ja_alocados))

    return len(simultaneos) == 0


def __is_simultaneos_callback__(i, periodo, turmas) -> bool:
    return i.dia == periodo.dia and i.ordem == periodo.ordem and __get_turno__(i.turma, turmas) == __get_turno__(
        periodo.turma, turmas)


def __get_turno__(turma_id: str, turmas: List[Turma]) -> str:
    return list(filter(lambda i: i.id == turma_id, turmas))[0].turno
