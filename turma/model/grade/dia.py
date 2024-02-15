from typing import List

from turma.model.grade.turma import GradeTurma


class GradeDia:
    id: str
    grade_turmas: List[GradeTurma]
