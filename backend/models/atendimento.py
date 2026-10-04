"""
Modelo de dados "Atendimento".

Este módulo NÃO conhece o MongoDB nem nenhuma camada superior (rotas,
serviços). Ele apenas define o formato de um Atendimento, as categorias
fixas permitidas e sabe converter esse formato de/para dicionário.

Importante: o sistema é administrativo, não clínico. Nenhum dado de
prontuário, anamnese ou informação de saúde é armazenado — apenas o
necessário para organizar a fila de atendimento do dia (nome do paciente,
tipo de atendimento, status e data/hora).
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

# Categorias fixas de tipo de atendimento (não é texto livre).
TIPOS_ATENDIMENTO = [
    "Consulta Geral",
    "Vacinação",
    "Curativo",
    "Encaminhamento",
]

# Estados possíveis do fluxo de atendimento (não é texto livre).
STATUS_VALIDOS = [
    "aguardando",
    "em atendimento",
    "finalizado",
]


@dataclass
class Atendimento:
    """Representa um atendimento registrado no posto de saúde/UPA.

    Atributos:
        nome_paciente: nome do paciente atendido.
        tipo_atendimento: uma das categorias fixas em TIPOS_ATENDIMENTO.
        status: uma das situações fixas em STATUS_VALIDOS.
        data_hora: data e hora do registro do atendimento (ISO 8601).
        id: identificador do documento no MongoDB (string do ObjectId).
    """

    nome_paciente: str
    tipo_atendimento: str
    status: str = "aguardando"
    data_hora: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    id: Optional[str] = None

    @staticmethod
    def from_dict(dados: dict) -> "Atendimento":
        """Cria um Atendimento a partir de um dicionário (ex.: JSON recebido na API)."""
        return Atendimento(
            nome_paciente=dados["nome_paciente"],
            tipo_atendimento=dados["tipo_atendimento"],
            status=dados.get("status") or "aguardando",
            data_hora=dados.get("data_hora") or datetime.utcnow().isoformat(),
            id=dados.get("id"),
        )

    def to_dict(self) -> dict:
        """Converte o Atendimento em um dicionário pronto para ser salvo no Mongo."""
        return {
            "nome_paciente": self.nome_paciente,
            "tipo_atendimento": self.tipo_atendimento,
            "status": self.status,
            "data_hora": self.data_hora,
        }

    def to_response(self) -> dict:
        """Converte o Atendimento em um dicionário pronto para ser retornado pela API."""
        dados = self.to_dict()
        dados["id"] = self.id
        return dados

    def validar(self) -> Optional[str]:
        """Valida os campos do atendimento.

        Retorna uma mensagem de erro (string) caso algo esteja inválido,
        ou None se o atendimento estiver válido.
        """
        if not self.nome_paciente or not self.nome_paciente.strip():
            return "O campo 'nome_paciente' é obrigatório."
        if self.tipo_atendimento not in TIPOS_ATENDIMENTO:
            opcoes = ", ".join(TIPOS_ATENDIMENTO)
            return f"O campo 'tipo_atendimento' deve ser um dos seguintes: {opcoes}."
        if self.status not in STATUS_VALIDOS:
            opcoes = ", ".join(STATUS_VALIDOS)
            return f"O campo 'status' deve ser um dos seguintes: {opcoes}."
        return None
