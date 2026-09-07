"""CA-24: executar testes não pode acessar o banco de uso manual."""
import os
from pathlib import Path
import sqlite3
import subprocess
import sys
import textwrap

import pytest


@pytest.mark.parametrize("url_configurada", [False, True])
def test_ca24_banco_manual_e_limpeza(tmp_path, url_configurada):
    banco_manual = tmp_path / "tarefas.db"
    with sqlite3.connect(banco_manual) as conexao:
        conexao.execute("CREATE TABLE sentinela (titulo TEXT)")
        conexao.execute("INSERT INTO sentinela VALUES ('Preservar')")
    conexao.close()
    original = banco_manual.read_bytes()
    ambiente = os.environ.copy()
    ambiente["PYTHONIOENCODING"] = "utf-8"
    ambiente.pop("TAREFAS_DATABASE_URL", None)
    if url_configurada:
        ambiente["TAREFAS_DATABASE_URL"] = f"sqlite:///{banco_manual}"

    projeto = Path(__file__).resolve().parents[1]
    codigo = """
        import os
        from pathlib import Path
        import sys
        import pytest

        banco_manual = Path(sys.argv[1]).resolve()
        projeto = Path(sys.argv[2])
        url_anterior = os.environ.get("TAREFAS_DATABASE_URL")

        def impedir_banco_manual(evento, argumentos):
            if evento == "sqlite3.connect":
                assert Path(argumentos[0]).resolve() != banco_manual, "Acesso ao banco manual"

        sys.addaudithook(impedir_banco_manual)
        arquivo = projeto / "tests" / "test_tarefas.py"
        resultado = pytest.main([
            str(arquivo) + "::test_ca01_cadastro_valido",
            str(arquivo) + "::test_ca09_lista_vazia",
            "-q", "-p", "no:cacheprovider", "--basetemp", "temporarios",
        ])
        assert resultado == 0

        from app import database
        from app.main import app

        assert app.dependency_overrides == {}
        assert os.environ.get("TAREFAS_DATABASE_URL") == url_anterior
        assert not Path(database.engine.url.database).parent.exists()
        assert not list(Path("temporarios").rglob("*.db"))
    """
    try:
        resultado = subprocess.run(
            [sys.executable, "-c", textwrap.dedent(codigo), str(banco_manual), str(projeto)],
            cwd=tmp_path, env=ambiente, capture_output=True, text=True,
            encoding="utf-8", timeout=60,
        )
        assert resultado.returncode == 0, resultado.stdout + resultado.stderr
        assert banco_manual.read_bytes() == original
    finally:
        banco_manual.unlink(missing_ok=True)
