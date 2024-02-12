from flask_restful import Resource

from service.organizacao import OrganizacaoService


class OrganizacaoController(Resource):
    def get(self) -> dict:
        return OrganizacaoService().perform()
