"""
Camada de rotas (Controller) para o recurso Atendimento.

Responsabilidade única desta camada: receber a requisição HTTP, extrair os
dados necessários, chamar o serviço correspondente e devolver a resposta
HTTP com o status code correto. Nenhuma regra de negócio ou acesso a banco
deve aparecer aqui.
"""

from flask import Blueprint, jsonify, request

from services.atendimento_service import AtendimentoService

atendimento_bp = Blueprint("atendimentos", __name__)

# A instância do serviço é definida em app.py e injetada aqui através de
# `init_atendimento_routes`, mantendo esta camada desacoplada de como o
# serviço é construído (qual repositório ele usa, etc.).
_atendimento_service: AtendimentoService = None


def init_atendimento_routes(atendimento_service: AtendimentoService) -> Blueprint:
    """Injeta o AtendimentoService que as rotas devem usar e retorna o Blueprint."""
    global _atendimento_service
    _atendimento_service = atendimento_service
    return atendimento_bp


@atendimento_bp.route("/atendimentos", methods=["GET"])
def listar_atendimentos():
    """GET /atendimentos — lista os atendimentos, com filtro opcional ?status=."""
    try:
        status = request.args.get("status")
        atendimentos = _atendimento_service.listar_atendimentos(status)
        return jsonify(atendimentos), 200
    except Exception as erro:
        return jsonify({"erro": f"Erro ao listar atendimentos: {erro}"}), 500


@atendimento_bp.route("/atendimentos/<string:atendimento_id>", methods=["GET"])
def buscar_atendimento(atendimento_id):
    """GET /atendimentos/<id> — retorna os detalhes de um atendimento específico."""
    try:
        atendimento = _atendimento_service.buscar_atendimento(atendimento_id)
        if atendimento is None:
            return jsonify({"erro": f"Atendimento com id '{atendimento_id}' não encontrado."}), 404
        return jsonify(atendimento), 200
    except Exception as erro:
        return jsonify({"erro": f"Erro ao buscar atendimento: {erro}"}), 500


@atendimento_bp.route("/atendimentos", methods=["POST"])
def criar_atendimento():
    """POST /atendimentos — registra um novo atendimento a partir do corpo JSON."""
    try:
        dados = request.get_json(force=True, silent=True)
        if not dados:
            return jsonify({"erro": "Corpo da requisição deve ser um JSON válido."}), 400

        atendimento_criado = _atendimento_service.criar_atendimento(dados)
        return jsonify(atendimento_criado), 201
    except ValueError as erro_validacao:
        return jsonify({"erro": str(erro_validacao)}), 400
    except KeyError as campo_faltante:
        return jsonify({"erro": f"Campo obrigatório ausente: {campo_faltante}"}), 400
    except Exception as erro:
        return jsonify({"erro": f"Erro ao registrar atendimento: {erro}"}), 500


@atendimento_bp.route("/atendimentos/<string:atendimento_id>", methods=["PUT"])
def atualizar_atendimento(atendimento_id):
    """PUT /atendimentos/<id> — atualiza um atendimento existente (ex.: status)."""
    try:
        dados = request.get_json(force=True, silent=True)
        if not dados:
            return jsonify({"erro": "Corpo da requisição deve ser um JSON válido."}), 400

        atendimento_atualizado = _atendimento_service.atualizar_atendimento(atendimento_id, dados)
        if atendimento_atualizado is None:
            return jsonify({"erro": f"Atendimento com id '{atendimento_id}' não encontrado."}), 404
        return jsonify(atendimento_atualizado), 200
    except ValueError as erro_validacao:
        return jsonify({"erro": str(erro_validacao)}), 400
    except KeyError as campo_faltante:
        return jsonify({"erro": f"Campo obrigatório ausente: {campo_faltante}"}), 400
    except Exception as erro:
        return jsonify({"erro": f"Erro ao atualizar atendimento: {erro}"}), 500


@atendimento_bp.route("/atendimentos/<string:atendimento_id>", methods=["DELETE"])
def remover_atendimento(atendimento_id):
    """DELETE /atendimentos/<id> — remove um registro de atendimento."""
    try:
        removido = _atendimento_service.remover_atendimento(atendimento_id)
        if not removido:
            return jsonify({"erro": f"Atendimento com id '{atendimento_id}' não encontrado."}), 404
        return jsonify({"mensagem": "Atendimento removido com sucesso."}), 200
    except Exception as erro:
        return jsonify({"erro": f"Erro ao remover atendimento: {erro}"}), 500
