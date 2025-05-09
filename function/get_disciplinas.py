from turma.function.get_turmas_map import get_turmas_map


def get_disciplinas() -> set[str]:
    turmas: set[str] = set()
    turmas_map: dict = get_turmas_map()
    for turma in turmas_map.values():
        for disciplina in turma.disciplina_map:
            turmas.add(disciplina)
        pass

    return turmas