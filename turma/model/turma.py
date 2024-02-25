from typing import List

from turma.model.disciplina import Disciplina


class Turma:
    turno: str
    disciplinas: List[Disciplina] = []
