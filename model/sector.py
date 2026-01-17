from typing import List

from model.cell import Cell


class Sector:
    turma: str = ''
    dia: str = ''
    cells: List[Cell] = []