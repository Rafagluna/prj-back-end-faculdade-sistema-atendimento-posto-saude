"""
Camada de acesso a dados (Repository) para o recurso Atendimento.

Aqui mora TODO o código que conversa diretamente com o MongoDB. Nenhuma
regra de negócio deve aparecer neste arquivo — apenas operações de
CRUD (criar, ler, atualizar, remover).

Princípios SOLID aplicados neste módulo:
- (S) Single Responsibility: a única responsabilidade desta classe é
  falar com o banco de dados.
- (L) Liskov Substitution: `AtendimentoRepositoryMongo` pode ser usada em
  qualquer lugar que espera um `AtendimentoRepositoryInterface` sem
  quebrar o comportamento esperado pela camada de serviço.
- (I) Interface Segregation: `AtendimentoRepositoryInterface` expõe
  apenas os métodos que a camada de serviço realmente usa.
- (D) Dependency Inversion: a camada de serviço depende da interface
  abstrata, não desta implementação concreta com MongoDB. Se um dia
  trocarmos o Mongo por outro banco, basta criar uma nova classe que
  implemente `AtendimentoRepositoryInterface` — o serviço não muda.
"""

from abc import ABC, abstractmethod
from typing import List, Optional

from bson import ObjectId
from bson.errors import InvalidId
from pymongo.collection import Collection

from models.atendimento import Atendimento


class AtendimentoRepositoryInterface(ABC):
    """Interface (contrato) que qualquer repositório de atendimentos deve seguir."""

    @abstractmethod
    def listar(self, status: Optional[str] = None) -> List[Atendimento]:
        """Lista todos os atendimentos, opcionalmente filtrando por status."""
        raise NotImplementedError

    @abstractmethod
    def buscar_por_id(self, atendimento_id: str) -> Optional[Atendimento]:
        """Busca um único atendimento pelo seu id."""
        raise NotImplementedError

    @abstractmethod
    def criar(self, atendimento: Atendimento) -> Atendimento:
        """Persiste um novo atendimento e retorna o atendimento criado (com id)."""
        raise NotImplementedError

    @abstractmethod
    def atualizar(self, atendimento_id: str, atendimento: Atendimento) -> Optional[Atendimento]:
        """Atualiza um atendimento existente. Retorna None se o id não existir."""
        raise NotImplementedError

    @abstractmethod
    def remover(self, atendimento_id: str) -> bool:
        """Remove um atendimento pelo id. Retorna True se algo foi removido."""
        raise NotImplementedError


class AtendimentoRepositoryMongo(AtendimentoRepositoryInterface):
    """Implementação do repositório de atendimentos usando MongoDB (pymongo)."""

    def __init__(self, colecao: Collection):
        """Recebe a Collection do pymongo já configurada (injeção de dependência)."""
        self._colecao = colecao

    def listar(self, status: Optional[str] = None) -> List[Atendimento]:
        filtro = {}
        if status:
            filtro["status"] = status

        documentos = self._colecao.find(filtro).sort("data_hora", -1)
        return [self._documento_para_atendimento(doc) for doc in documentos]

    def buscar_por_id(self, atendimento_id: str) -> Optional[Atendimento]:
        object_id = self._converter_para_object_id(atendimento_id)
        if object_id is None:
            return None

        documento = self._colecao.find_one({"_id": object_id})
        return self._documento_para_atendimento(documento) if documento else None

    def criar(self, atendimento: Atendimento) -> Atendimento:
        resultado = self._colecao.insert_one(atendimento.to_dict())
        atendimento.id = str(resultado.inserted_id)
        return atendimento

    def atualizar(self, atendimento_id: str, atendimento: Atendimento) -> Optional[Atendimento]:
        object_id = self._converter_para_object_id(atendimento_id)
        if object_id is None:
            return None

        resultado = self._colecao.update_one({"_id": object_id}, {"$set": atendimento.to_dict()})
        if resultado.matched_count == 0:
            return None

        atendimento.id = atendimento_id
        return atendimento

    def remover(self, atendimento_id: str) -> bool:
        object_id = self._converter_para_object_id(atendimento_id)
        if object_id is None:
            return False

        resultado = self._colecao.delete_one({"_id": object_id})
        return resultado.deleted_count > 0

    @staticmethod
    def _converter_para_object_id(atendimento_id: str) -> Optional[ObjectId]:
        """Converte uma string para ObjectId, retornando None se for inválida."""
        try:
            return ObjectId(atendimento_id)
        except (InvalidId, TypeError):
            return None

    @staticmethod
    def _documento_para_atendimento(documento: dict) -> Atendimento:
        """Converte um documento do MongoDB em uma instância de Atendimento."""
        return Atendimento(
            id=str(documento["_id"]),
            nome_paciente=documento["nome_paciente"],
            tipo_atendimento=documento["tipo_atendimento"],
            status=documento["status"],
            data_hora=documento["data_hora"],
        )
