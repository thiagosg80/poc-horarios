from typing import List

from turma.model.grade.dia import GradeDia


class GradeTurno:
    id: str
    dias_da_semana: List[GradeDia] = []
