from flask import Response

from function.get_dias_da_semana import get_dias_da_semana
from function.to_grade import to_grade
from professor.function.get_professores import get_professores
from turma.function.get_periodos import get_periodos
from turma.function.get_turmas_map import get_turmas_map
from turma.function.get_turnos_grade import get_turnos_grade
from turma.function.grade.get_grade_file import get_grade_file
from function.set_organizacao import set_organizacao


def perform_organizacao() -> Response:
    turmas_map = get_turmas_map()
    dias_da_semana = get_dias_da_semana()
    periodos = get_periodos(list(map(lambda key: key, turmas_map)), dias_da_semana)
    turnos_grade = get_turnos_grade(turmas_map, dias_da_semana, periodos)
    professores = get_professores(turmas_map)
    set_organizacao(professores, turmas_map, turnos_grade)
    grade: dict = to_grade(turnos_grade, periodos)

    return get_grade_file(grade, 'resource/grade.html')