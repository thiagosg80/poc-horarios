from typing import List

from turma.model.grade.aula import Aula


class TurnoDia:
    id: str
    aulas: List[Aula]
