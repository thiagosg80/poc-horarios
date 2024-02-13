from flask_restful import Resource

from function.perform_organizacao import perform_organizacao


class OrganizacaoController(Resource):
    def get(self) -> dict:
        return perform_organizacao()
