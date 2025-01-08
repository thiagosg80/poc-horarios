from flask import Response, send_file

from turma.function.write_file import write_file


def get_grade_file(input: dict, resource_name: str) -> Response:
    write_file(input, resource_name)

    return send_file(resource_name)
