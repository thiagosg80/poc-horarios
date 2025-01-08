from typing import List

from turma.function.get_indexes_groups import get_indexes_groups


def get_grades_by_dias(dias_by_sectors, turmas_by_turno, turmas_map, aulas) -> List[dict]:
    indexes_groups = get_indexes_groups(dias_by_sectors, 'possibilidades')
    grades = []
    quantidade_periodos_map: dict = {}

    for turma in turmas_by_turno:
        disciplina: str = next(filter(lambda x: x.turma == turma, aulas)).disciplina
        quantidade_periodos: int = turmas_map.get(turma).disciplina_map.get(disciplina).quantidade_periodos

        quantidade_periodos_map[turma] = {
            'quantidade_periodos': quantidade_periodos,
            'quantidade_periodos_na_possibilidade': 0
        }

    for indexes in indexes_groups:
        possibilidade_by_dia: dict = {}

        for item in list(quantidade_periodos_map.values()):
            item['quantidade_periodos_na_possibilidade'] = 0

        for i, cell_index in enumerate(indexes):
            container = dias_by_sectors[i]
            possibilidade: dict = container['possibilidades'][cell_index]
            possibilidade_by_dia[container['dia']] = possibilidade

        if __is_possible(quantidade_periodos_map, possibilidade_by_dia, turmas_by_turno):
            grades.append(possibilidade_by_dia)

    return grades

def __is_possible(quantidade_periodos_map, possibilidade_by_dia, turmas_by_turno) -> bool:
    for possibilidade in list(possibilidade_by_dia.values()):
        for turma_by_turno in turmas_by_turno:
            quantidade_map = quantidade_periodos_map.get(turma_by_turno)

            quantidade_map['quantidade_periodos_na_possibilidade'] += (possibilidade.get(turma_by_turno)
                                                                       .get('quantidade_periodos_alocados'))

    for item in list(quantidade_periodos_map.values()):
        if item['quantidade_periodos_na_possibilidade'] != item['quantidade_periodos']:
            return False

    return True