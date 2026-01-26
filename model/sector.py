from typing import List

from model.cell import Cell


class Sector:
    turma: str = ''
    dia: str = ''
    cells: List[Cell] = []
    quantidade_periodos_alocados: int = 0