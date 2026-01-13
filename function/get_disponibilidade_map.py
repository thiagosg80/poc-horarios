from professor.model.disponibilidade import Disponibilidade


def get_disponibilidade_map(disponibilidades: list[Disponibilidade], turno: str) -> dict:
    disponibilidade_map: dict = __get_disponibilidade_map(disponibilidades)

    return disponibilidade_map.get(turno)

def __get_disponibilidade_map(disponibilidades: list[Disponibilidade]) -> dict:
    turnos: set[str] = set(map(lambda x: x.turno, disponibilidades))

    return {turno: __get_disponibilidades_by_turno(turno, disponibilidades) for turno in turnos}

def __get_disponibilidades_by_turno(turno: str, disponibilidades: list[Disponibilidade]) -> dict:
    filtered: list[Disponibilidade] = list(filter(lambda d: d.turno == turno, disponibilidades))
    dias: list[str] = list(map(lambda x: x.dia, filtered))

    return {dia: list(filter(lambda i: i.dia == dia, filtered))[0].quantidade_de_periodos for dia in dias}