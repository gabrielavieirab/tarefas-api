"""SQLite temporário por teste, inclusive durante a inicialização da API."""
import os
import tempfile
from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import sessionmaker

# A aplicação lê a URL ao importar; proteja também o banco usado pelo lifespan.
_url_anterior = os.environ.get("TAREFAS_DATABASE_URL")
_pasta_banco = tempfile.TemporaryDirectory(prefix="tarefas-testes-")
os.environ["TAREFAS_DATABASE_URL"] = (
    f"sqlite:///{Path(_pasta_banco.name) / 'inicializacao.db'}"
)

from app import database  # noqa: E402
from app.main import app  # noqa: E402


def pytest_unconfigure(config):
    # Fechar antes de apagar evita arquivo em uso no Windows.
    try:
        database.engine.dispose()
        _pasta_banco.cleanup()
    finally:
        if _url_anterior is None:
            os.environ.pop("TAREFAS_DATABASE_URL", None)
        else:
            os.environ["TAREFAS_DATABASE_URL"] = _url_anterior


@pytest.fixture
def cliente(tmp_path):
    caminho_banco = tmp_path / "teste_tarefas.db"
    engine = database.criar_engine(f"sqlite:///{caminho_banco}")
    SessaoTeste = sessionmaker(bind=engine)
    overrides_anteriores = app.dependency_overrides.copy()

    def get_db_teste():
        with SessaoTeste() as sessao:
            yield sessao

    try:
        database.init_db(engine)
        app.dependency_overrides[database.get_db] = get_db_teste
        with TestClient(app) as client:
            yield client
    finally:
        app.dependency_overrides.clear()
        app.dependency_overrides.update(overrides_anteriores)
        engine.dispose()
        caminho_banco.unlink(missing_ok=True)
