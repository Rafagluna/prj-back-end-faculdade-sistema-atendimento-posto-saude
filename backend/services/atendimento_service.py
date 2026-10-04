"""
Camada de regras de negócio (Service) para o recurso Atendimento.

Esta classe orquestra as operações de atendimento. Tudo que envolve banco
de dados é delegado ao repositório; tudo que envolve HTTP é
responsabilidade das rotas.

Princípio de Inversão de Dependência (D do SOLID):
O `AtendimentoService` depende apenas da abstração
`AtendimentoRepositoryInterface`, recebida via injeção de dependência no
construtor. Ele não sabe (e não precisa saber) que por trás dessa
interface existe um MongoDB.
"""

from typing import List, Optional

from models.atendimento import Atendimento
from repositories.atendimento_repository import AtendimentoRepositoryInterface


class AtendimentoService:
    """Implementa as regras de negócio relacionadas aos atendimentos."""

    def __init__(self, repositorio: AtendimentoRepositoryInterface):
        """Recebe o repositório de atendimentos por injeção de dependência."""
        self._repositorio = repositorio

    def listar_atendimentos(self, status: Optional[str] = None) -> List[dict]:
        """Retorna todos os atendimentos cadastrados, opcionalmente filtrados por status."""
        atendimentos = self._repositorio.listar(status)
        return [atendimento.to_response() for atendimento in atendimentos]

    def buscar_atendimento(self, atendimento_id: str) -> Optional[dict]:
        """Retorna os detalhes de um atendimento pelo id, ou None se não existir."""
        atendimento = self._repositorio.buscar_por_id(atendimento_id)
        return atendimento.to_response() if atendimento else None

    def criar_atendimento(self, dados: dict) -> dict:
        """Valida e registra um novo atendimento.

        Levanta ValueError com uma mensagem amigável caso os dados sejam
        inválidos, para que a rota converta isso em um HTTP 400.
        """
        atendimento = Atendimento.from_dict(dados)
        erro = atendimento.validar()
        if erro:
            raise ValueError(erro)

        atendimento_criado = self._repositorio.criar(atendimento)
        return atendimento_criado.to_response()

    def atualizar_atendimento(self, atendimento_id: str, dados: dict) -> Optional[dict]:
        """Valida e atualiza um atendimento existente (ex.: mudança de status).

        Retorna None se o atendimento não existir.
        """
        atendimento = Atendimento.from_dict(dados)
        erro = atendimento.validar()
        if erro:
            raise ValueError(erro)

        atendimento_atualizado = self._repositorio.atualizar(atendimento_id, atendimento)
        return atendimento_atualizado.to_response() if atendimento_atualizado else None

    def remover_atendimento(self, atendimento_id: str) -> bool:
        """Remove um atendimento pelo id. Retorna True se a remoção ocorreu."""
        return self._repositorio.remover(atendimento_id)
