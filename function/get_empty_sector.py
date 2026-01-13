from function.get_empty_cells import get_empty_cells
from model.sector import Sector


def get_empty_sector(quantidade_de_periodos: list[int]) -> Sector:
    sector: Sector = Sector()
    sector.cells = get_empty_cells(quantidade_de_periodos)

    return sector