def get_converted_grades_by_dia(grades_input: list[dict]) -> list[dict]:
    converted_grades = []
    for grade_tuple in grades_input:
        converted_grade = {}
        for day_schedule in grade_tuple:
            if day_schedule:
                # Get the day from the first sector object in the dictionary
                first_turma = next(iter(day_schedule))
                dia = day_schedule[first_turma].dia
                converted_grade[dia] = day_schedule
        if converted_grade:
            converted_grades.append(converted_grade)
    return converted_grades