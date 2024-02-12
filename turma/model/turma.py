from typing import List

from turma.model.disciplina import Disciplina


class Turma:
    id: str
    disciplinas: List[Disciplina] = []
