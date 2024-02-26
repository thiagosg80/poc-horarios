from typing import List

from professor.function.get_professores import get_professores
from professor.model.aula import Aula
from professor.model.disponibilidade import Disponibilidade
from professor.model.professor import Professor
from turma.function.get_turmas_map import get_turmas_map
from turma.model.grade.periodo import Periodo


def set_organizacao(professores: List[Professor], periodos: List[Periodo], turmas_map: dict) -> None:
    for professor in professores:
        i = 0
        trocou_o_professor = True
        periodo_descricao = professor.disciplina + ' - ' + professor.nome
        while __tem_disponibilidade__(professor.disponibilidades) and i < 5:
            if not trocou_o_professor:
                __reiniciar__(professor, periodos, turmas_map, periodo_descricao)

            trocou_o_professor = False
            __organizar__(professor, periodos, turmas_map, periodo_descricao)
            __set_marcacoes_consecutivas__(professor, turmas_map)
            i += 1


def __tem_disponibilidade__(disponibilidades_input: List[Disponibilidade]) -> bool:
    filtered = list(filter(lambda i: i.quantidade_de_periodos, disponibilidades_input))

    return len(filtered) > 0


def __reiniciar__(professor: Professor, periodos: List[Periodo], turmas_map: dict, periodo_descricao: str) -> None:
    for periodo in list(filter(lambda i: i.descricao == periodo_descricao, periodos)):
        periodo.descricao = ''

    professores = get_professores(turmas_map)
    filtered = list(filter(lambda i: i.nome == professor.nome, professores))[0]
    for d in filtered.disponibilidades:
        disponibilidade = list(filter(lambda i: i.dia == d.dia and i.turno == d.turno, professor.disponibilidades))[0]
        disponibilidade.quantidade_de_periodos = d.quantidade_de_periodos

    turmas_map_valores_originais = get_turmas_map()
    for key, value in turmas_map.items():
        turma_map_valor_original = turmas_map_valores_originais.get(key)
        for disciplina_key, disciplina_value in value.disciplina_map.items():
            disciplina_map_valor_original = turma_map_valor_original.disciplina_map.get(disciplina_key)
            disciplina_value.quantidade_periodos = disciplina_map_valor_original.quantidade_periodos


def __organizar__(professor: Professor, periodos: List[Periodo], turmas_map: dict, periodo_descricao: str) -> None:
    dias_disponiveis = list(map(lambda i: i.dia, professor.disponibilidades))
    turmas = list(map(lambda i: i.turma, professor.aulas))
    periodos_filtrados = list(filter(lambda i: i.dia in dias_disponiveis and i.turma in turmas, periodos))
    periodos_ja_alocados = []
    for periodo in periodos_filtrados:
        turma = turmas_map[periodo.turma]
        disciplina = turma.disciplina_map.get(professor.disciplina)

        disponibilidade = __get_disponibilidade__(professor, turma.turno, periodo.dia) \
            if disciplina.quantidade_periodos > 0 else __get_empty_disponibilidade__()

        quantidade_maxima_periodos_consecutivos = (list(filter(
            lambda i: i.turma == periodo.turma and i.disciplina == professor.disciplina, professor.aulas))[0]
                                                   .quantidade_maxima_periodos_consecutivos)

        if (disponibilidade.quantidade_de_periodos > 0 and __nao_tem_marcacoes_consecutivas_ainda__(
                quantidade_maxima_periodos_consecutivos, periodos_filtrados, periodo.turma, periodo.dia,
                periodo_descricao) and disciplina.quantidade_periodos > 0 and not periodo.descricao and
                __nao_ha_periodos_simultaneos__(periodos_ja_alocados, periodo, turmas_map)):

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


def __nao_ha_periodos_simultaneos__(periodos_ja_alocados: List[Periodo], periodo: Periodo, turmas_map: dict) -> bool:
    simultaneos = list(filter(lambda i: __is_simultaneos_callback__(i, periodo, turmas_map), periodos_ja_alocados))

    return len(simultaneos) == 0


def __is_simultaneos_callback__(i: Periodo, periodo: Periodo, turmas_map: dict) -> bool:
    is_same_turno = turmas_map[i.turma].turno == turmas_map[periodo.turma].turno

    return i.dia == periodo.dia and i.ordem == periodo.ordem and is_same_turno


def __set_marcacoes_consecutivas__(professor: Professor, turmas_map: dict) -> None:
    aulas_pendentes: List[Aula] = []
    for aula in professor.aulas:
        turma = turmas_map[aula.turma]
        disciplina = turma.disciplina_map.get(aula.disciplina)
        if disciplina.quantidade_periodos:
            aulas_pendentes.append(aula)

    turmas_pendentes = list(map(lambda i: i.turma, aulas_pendentes))

    aulas_a_reduzir_quantidade_periodos_consecutivos = list(filter(lambda i: i.turma not in turmas_pendentes,
                                                                   professor.aulas))

    for aula_a_reduzir in aulas_a_reduzir_quantidade_periodos_consecutivos:
        aula_a_reduzir.quantidade_maxima_periodos_consecutivos -= 1

    pass
