from typing import List

from turma.function.get_periodos_ordens import get_periodos_ordens
from turma.model.grade.periodo import Periodo


def get_periodos(turmas_ids: List[str], dias: List[str]) -> List[Periodo]:
    periodos = []
    periodos_ordens = get_periodos_ordens()
    [__add_periodos__(periodos, turma_id, dias, periodos_ordens) for turma_id in turmas_ids]

    return periodos


def __add_periodos__(periodos: List[Periodo], turma_id: str, dias: List[str], periodos_ordens: List[int]) -> None:
    for dia in dias:
        for ordem in periodos_ordens:
            __add_periodo__(periodos, turma_id, dia, ordem)


def __add_periodo__(periodos: List[Periodo], turma_id: str, dia: str, ordem: int) -> None:
    periodo = Periodo()
    periodo.turma = turma_id
    periodo.dia = dia
    periodo.ordem = ordem
    periodos.append(periodo)
