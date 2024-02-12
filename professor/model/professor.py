from typing import List

from professor.model.disponibilidade import Disponibilidade


class Professor:
    nome: str
    disciplina: str
    turmas: List[str] = []
    disponibilidades: List[Disponibilidade] = []
