"""Configuração do banco de dados SQLite para a API de tarefas.

Implementa a ADR-002 (docs/decisoes_tecnicas.md): SQLite em arquivo local,
acessado de forma síncrona pelo SQLAlchemy 2, com um engine por aplicação
e uma sessão por requisição. A URL é configurável por variável de
ambiente para permitir um banco de teste independente do banco de uso
manual (RNF-02 / ADR-004), sem exigir mudança de código.
"""
import os
from typing import Generator

from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

# Banco de uso manual: arquivo local reutilizado entre reinicializações
# (RN-11). Os testes devem usar `criar_engine` com uma URL de arquivo
# temporário próprio, nunca este arquivo.
DATABASE_URL = os.getenv("TAREFAS_DATABASE_URL", "sqlite:///./tarefas.db")


class Base(DeclarativeBase):
    """Base declarativa dos modelos ORM do projeto (ver app/models.py)."""


def criar_engine(database_url: str = DATABASE_URL) -> Engine:
    """Cria um engine SQLAlchemy para a URL informada.

    `check_same_thread=False` é necessário apenas para SQLite: o FastAPI
    pode acessar a mesma conexão a partir de threads diferentes das rotas
    síncronas (ver ADR-002). Para outros bancos, o argumento é omitido.
    """
    connect_args = {"check_same_thread": False} if database_url.startswith("sqlite") else {}
    return create_engine(database_url, connect_args=connect_args)


# Engine e fábrica de sessões padrão da aplicação, ligados ao banco de uso
# manual. Os testes constroem seu próprio engine/sessão com `criar_engine`
# apontando para um arquivo temporário (ver tests/test_models.py).
engine = criar_engine()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db(engine_: Engine = engine) -> None:
    """Cria as tabelas declaradas em `Base.metadata`, se ainda não existirem.

    Importa `app.models` antes de criar as tabelas: uma classe só registra
    sua tabela em `Base.metadata` quando o módulo que a declara é
    importado. Sem isso, chamar esta função sem que `app.models` já
    tenha sido importado em outro ponto criaria um banco sem tabelas.
    """
    from app import models  # noqa: F401  (import necessário pelo efeito colateral)

    Base.metadata.create_all(bind=engine_)


def get_db() -> Generator[Session, None, None]:
    """Fornece uma sessão por requisição e garante o fechamento (ADR-002).

    Uso previsto como dependência do FastAPI (`Depends(get_db)`) quando as
    rotas forem implementadas; a dependência pode ser substituída nos
    testes por uma sessão ligada a um banco temporário (RNF-02).
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
