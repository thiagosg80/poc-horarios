from flask import Response, send_file

from turma.function.write_file import write_file


def get_grade_file(grade_input: dict, resource_name: str) -> Response:
    write_file(grade_input, resource_name)

    return send_file(resource_name)
