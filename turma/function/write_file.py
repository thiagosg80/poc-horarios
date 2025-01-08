from flask import render_template

def write_file(grade_input: dict, resource_name: str) -> None:
    file = open(resource_name, 'w')
    file.write(render_template('grade.html', grade_input=grade_input))
    file.close()