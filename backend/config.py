"""
Configurações centrais da aplicação.

Mantém em um único lugar tudo que é específico de ambiente (conexão com o
banco, portas, flags), para que nenhum outro módulo precise saber de onde
essas informações vêm (variáveis de ambiente, valores padrão, etc.).
"""

import os


class Config:
    """Agrupa as configurações usadas pela aplicação Flask."""

    MONGO_URI = os.environ.get("MONGO_URI", "mongodb://mongo:27017/posto_saude")
    MONGO_DB_NAME = os.environ.get("MONGO_DB_NAME", "posto_saude")
    DEBUG = os.environ.get("FLASK_DEBUG", "true").lower() == "true"
    PORT = int(os.environ.get("PORT", 5000))
