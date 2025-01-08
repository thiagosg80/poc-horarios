def fit(combined_grades, grade_template, grade_index: int) -> None:
    for turno in grade_template:
        for dia_da_semana in turno.dias_da_semana:
            for grade_turma in dia_da_semana.grade_turmas:
                for periodo in grade_turma.periodos:
                    combined = combined_grades[turno.id]
                    possibility = combined[grade_index]
                    if periodo.dia in possibility:
                        possible_day = possibility[periodo.dia]
                        possible_turma = possible_day[periodo.turma]
                        possible_periodo = [ x for x in possible_turma['cells'] if x['periodo'] == periodo.ordem][0]
                        periodo.descricao = possible_periodo['allocated']