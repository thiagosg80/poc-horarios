from model.cell import Cell


def fit(combined_grades, grade_template, grade_index: int) -> None:
    for turno in grade_template:
        for dia_da_semana in turno.dias_da_semana:
            for grade_turma in dia_da_semana.grade_turmas:
                for periodo in grade_turma.periodos:
                    if turno.id in combined_grades:
                        combined = combined_grades[turno.id]
                        possibility = combined[grade_index]
                        if periodo.dia in possibility:
                            possible_day = possibility[periodo.dia]
                            if periodo.turma in possible_day:
                                possible_turma = possible_day[periodo.turma]

                                possible_periodo = [x for x in possible_turma['cells'] if isinstance(x, dict) and x['periodo'] == periodo.ordem or isinstance(x, Cell) and x.position == periodo.ordem][0]

                                periodo.descricao = possible_periodo['allocated'] if isinstance(possible_periodo, dict) else possible_periodo.allocation