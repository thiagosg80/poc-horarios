from flask import Response, send_file, render_template


def get_grade_file(input: dict) -> Response:
    file_name = 'grade.html'
    resource_name = 'resource/grade.html'
    file = open(resource_name, 'w')
    file.write(render_template(file_name, grade_input=input))
    file.close()

    return send_file(resource_name)
