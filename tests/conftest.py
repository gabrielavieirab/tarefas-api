"""Configuração compartilhada dos testes da API.

Fixa a URL do banco de uso manual para um arquivo descartável ANTES de
importar `app.main`/`app.database`: a URL é lida uma única vez, na
importação do módulo (variável de nível de módulo), então isso precisa
acontecer primeiro para garantir que a suíte nunca crie, leia ou altere o
`tarefas.db` real (RNF-02 / CA-24). Cada teste, além disso, recebe seu
próprio arquivo temporário via a fixture `cliente`.

Não usamos `tempfile.TemporaryDirectory()` para esse arquivo descartável:
seu finalizador tenta apagar a pasta na saída do processo, e no Windows
isso falha com `PermissionError: [WinError 32]` se o SQLite ainda tiver o
arquivo aberto (o pool de conexões do engine só é fechado explicitamente
por `_fechar_engine_padrao_ao_final`, abaixo, e a ordem entre isso e o
finalizador do `TemporaryDirectory` não é garantida). Um caminho comum
dentro da pasta temporária do sistema, sem autolimpeza, evita o problema;
sobra um arquivo pequeno no temp do SO, sem risco (nunca é lido).
"""
import os
import tempfile
import uuid

_CAMINHO_BANCO_PADRAO_TESTES = os.path.join(
    tempfile.gettempdir(), f"tarefas_api_nao_usar_{uuid.uuid4().hex}.db"
)
os.environ["TAREFAS_DATABASE_URL"] = f"sqlite:///{_CAMINHO_BANCO_PADRAO_TESTES}"

import pytest  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402
from sqlalchemy.orm import sessionmaker  # noqa: E402

from app import database as _database  # noqa: E402
from app.database import criar_engine, get_db, init_db  # noqa: E402
from app.main import app  # noqa: E402


@pytest.fixture(scope="session", autouse=True)
def _fechar_engine_padrao_ao_final():
    """Fecha o engine padrão (usado só pelo `lifespan` do FastAPI a cada
    TestClient criado) ao fim da sessão de testes, liberando o arquivo
    descartável antes do processo encerrar."""
    yield
    _database.engine.dispose()


@pytest.fixture
def cliente(tmp_path):
    """TestClient com banco SQLite temporário, limpo e isolado por teste."""
    caminho_banco = tmp_path / "teste_tarefas.db"
    engine = criar_engine(f"sqlite:///{caminho_banco}")
    init_db(engine)
    SessaoTeste = sessionmaker(bind=engine)

    def get_db_teste():
        sessao = SessaoTeste()
        try:
            yield sessao
        finally:
            sessao.close()

    app.dependency_overrides[get_db] = get_db_teste
    try:
        with TestClient(app) as client:
            yield client
    finally:
        app.dependency_overrides.clear()
        engine.dispose()
