from typing import List

from turma.model.grade.dia import TurnoDia


class GradeTurno:
    id: str
    dias_da_semana: List[TurnoDia] = []
