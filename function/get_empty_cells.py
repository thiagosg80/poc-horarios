from model.cell import Cell


def get_empty_cells(quantidade_de_periodos: list[int]) -> list[Cell]:
    return list(map(lambda x: __get_cell(x), quantidade_de_periodos))

def __get_cell(position: int) -> Cell:
    cell: Cell = Cell()
    cell.position = position

    return cell