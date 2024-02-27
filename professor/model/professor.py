from typing import List

from professor.model.aula import Aula
from professor.model.disponibilidade import Disponibilidade


class Professor:
    nome: str
    disciplina: str
    aulas: List[Aula] = []
    disponibilidades: List[Disponibilidade] = []
