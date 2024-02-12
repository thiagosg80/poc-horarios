from flask import Flask
from flask_restful import Api

from controller.organizacao import OrganizacaoController

app = Flask(__name__)
api = Api(app)


api.add_resource(OrganizacaoController, '/horarios/organizar')


if __name__ == '__main__':
    app.run()
