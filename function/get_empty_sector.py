from typing import List

from model.cell import Cell
from model.sector import Sector


def get_empty_sector(quantidade_de_periodos: List[int]) -> Sector:
    sector: Sector = Sector()
    sector.cells = list(map(lambda x: __get_cell(x), quantidade_de_periodos))

    return sector


def __get_cell(position: int) -> Cell:
    cell: Cell = Cell()
    cell.position = position

    return cell