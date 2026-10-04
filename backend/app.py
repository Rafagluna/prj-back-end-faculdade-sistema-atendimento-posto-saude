"""
Ponto de entrada da aplicação Flask.

Este arquivo é o único lugar responsável por "montar" a aplicação: conectar
ao MongoDB, instanciar o repositório concreto, injetá-lo no serviço e
registrar as rotas. É aqui que a Inversão de Dependência (D do SOLID)
acontece na prática — se um dia quisermos trocar o MongoDB por outro
banco, a troca acontece SOMENTE nestas poucas linhas.
"""

from flask import Flask, jsonify
from flask_cors import CORS
from pymongo import MongoClient

from config import Config
from repositories.atendimento_repository import AtendimentoRepositoryMongo
from routes.atendimento_routes import init_atendimento_routes
from services.atendimento_service import AtendimentoService


def criar_app() -> Flask:
    """Cria e configura a instância da aplicação Flask (application factory)."""
    app = Flask(__name__)
    CORS(app)

    cliente_mongo = MongoClient(Config.MONGO_URI)
    banco = cliente_mongo[Config.MONGO_DB_NAME]
    colecao_atendimentos = banco["atendimentos"]

    # Composição das camadas: repositório concreto -> serviço -> rotas.
    repositorio_atendimentos = AtendimentoRepositoryMongo(colecao_atendimentos)
    servico_atendimentos = AtendimentoService(repositorio_atendimentos)

    app.register_blueprint(init_atendimento_routes(servico_atendimentos))

    @app.route("/health", methods=["GET"])
    def health_check():
        """Endpoint simples para verificar se a API está no ar."""
        return jsonify({"status": "ok"}), 200

    return app


app = criar_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=Config.PORT, debug=Config.DEBUG)
