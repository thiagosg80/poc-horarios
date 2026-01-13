def get_converted_grades_by_dia(grades_input: list[dict]):
    converted_grades = []
    for grade in grades_input:
        converted_grade = {}
        for turma, dias in grade.items():
            for dia, cells in dias.items():
                if dia not in converted_grade:
                    converted_grade[dia] = {}
                converted_grade[dia][turma] = cells
        converted_grades.append(converted_grade)

    return converted_grades