"""Cenários de aceitação da API (docs/criterios_aceitacao.md, CA-01 a CA-31).

Cada teste referencia o(s) critério(s)/regra(s) que cobre. Usa a fixture
`cliente` (tests/conftest.py): banco SQLite temporário e limpo por teste.
"""
import json
import os
from pathlib import Path
import subprocess
import sys
import textwrap

import pytest

MENSAGEM_NAO_ENCONTRADA = "Tarefa não encontrada."
ID_MAXIMO = 9_223_372_036_854_775_807


def _cadastrar(cliente, titulo="Estudar"):
    resposta = cliente.post("/tarefas", json={"titulo": titulo})
    assert resposta.status_code == 201
    return resposta.json()


# ---------------------------------------------------------------- Cadastro

def test_ca01_cadastro_valido(cliente):
    resposta = cliente.post("/tarefas", json={"titulo": "Estudar"})
    assert resposta.status_code == 201
    corpo = resposta.json()
    assert isinstance(corpo["id"], int) and corpo["id"] > 0
    assert corpo["titulo"] == "Estudar"
    assert corpo["concluida"] is False

    listagem = cliente.get("/tarefas").json()
    assert corpo in listagem


@pytest.mark.parametrize("titulo", ["  Revisar API  ", "  Revisar  português  "])
def test_ca02_normalizacao_do_titulo(cliente, titulo):
    resposta = cliente.post("/tarefas", json={"titulo": titulo})
    assert resposta.status_code == 201
    assert resposta.json()["titulo"] == titulo.strip()
    assert cliente.get("/tarefas").json() == [resposta.json()]


@pytest.mark.parametrize("titulo", ["", "   ", "\t\n"])
def test_ca03_titulo_ausente_ou_vazio(cliente, titulo):
    resposta = cliente.post("/tarefas", json={"titulo": titulo})
    assert resposta.status_code == 422
    assert any(erro["loc"] == ["body", "titulo"] for erro in resposta.json()["detail"])
    assert cliente.get("/tarefas").json() == []


def test_ca03_titulo_ausente_do_corpo(cliente):
    resposta = cliente.post("/tarefas", json={})
    assert resposta.status_code == 422
    assert any(erro["loc"] == ["body", "titulo"] for erro in resposta.json()["detail"])
    assert cliente.get("/tarefas").json() == []


@pytest.mark.parametrize("titulo", [None, 123, True, ["a"], {"x": 1}])
def test_ca04_tipo_invalido_de_titulo(cliente, titulo):
    resposta = cliente.post("/tarefas", json={"titulo": titulo})
    assert resposta.status_code == 422
    assert cliente.get("/tarefas").json() == []


@pytest.mark.parametrize("caractere", ["a", "á"])
def test_ca05_limites_do_titulo(cliente, caractere):
    for titulo in (caractere, caractere * 120, f"  {caractere * 120}  "):
        resposta = cliente.post("/tarefas", json={"titulo": titulo})
        assert resposta.status_code == 201
        assert resposta.json()["titulo"] == titulo.strip()
        assert resposta.json() in cliente.get("/tarefas").json()

    antes = cliente.get("/tarefas").json()
    resposta = cliente.post("/tarefas", json={"titulo": caractere * 121})
    assert resposta.status_code == 422
    assert cliente.get("/tarefas").json() == antes


@pytest.mark.parametrize("campo_extra", ["id", "concluida", "prioridade"])
def test_ca06_campos_controlados_pelo_servidor(cliente, campo_extra):
    corpo = {"titulo": "Estudar", campo_extra: 1}
    resposta = cliente.post("/tarefas", json=corpo)
    assert resposta.status_code == 422
    assert any(erro["loc"] == ["body", campo_extra] for erro in resposta.json()["detail"])
    assert cliente.get("/tarefas").json() == []


def test_ca07_titulos_repetidos_geram_tarefas_distintas(cliente):
    primeira = _cadastrar(cliente, "Mesmo título")
    segunda = _cadastrar(cliente, "Mesmo título")
    assert primeira["id"] != segunda["id"]
    assert len(cliente.get("/tarefas").json()) == 2


def test_ca08_corpo_ausente_ou_json_malformado(cliente):
    sem_corpo = cliente.post("/tarefas")
    assert sem_corpo.status_code == 422

    malformado = cliente.post(
        "/tarefas",
        content=b'{"titulo": "Estudar"',
        headers={"Content-Type": "application/json"},
    )
    assert malformado.status_code == 422
    assert cliente.get("/tarefas").json() == []


# ---------------------------------------------------------------- Listagem

def test_ca09_lista_vazia(cliente):
    resposta = cliente.get("/tarefas")
    assert resposta.status_code == 200
    assert resposta.json() == []


def test_ca10_lista_com_estados_diferentes_em_ordem_crescente(cliente):
    t1 = _cadastrar(cliente, "Primeira")
    t2 = _cadastrar(cliente, "Segunda")
    assert cliente.patch(f"/tarefas/{t1['id']}", json={"concluida": True}).status_code == 200

    listagem = cliente.get("/tarefas").json()
    assert [t["id"] for t in listagem] == sorted(t["id"] for t in listagem)
    assert [t["id"] for t in listagem] == [t1["id"], t2["id"]]
    assert {t["id"]: t["concluida"] for t in listagem} == {t1["id"]: True, t2["id"]: False}
    assert all(set(t.keys()) == {"id", "titulo", "concluida"} for t in listagem)


def test_ca11_leitura_nao_altera_registros(cliente):
    _cadastrar(cliente, "Estudar")
    primeira_leitura = cliente.get("/tarefas").json()
    segunda_leitura = cliente.get("/tarefas").json()
    assert primeira_leitura == segunda_leitura


# --------------------------------------------------------------- Conclusão

def test_ca12_concluir_tarefa_pendente(cliente):
    tarefa = _cadastrar(cliente)
    resposta = cliente.patch(f"/tarefas/{tarefa['id']}", json={"concluida": True})
    assert resposta.status_code == 200
    corpo = resposta.json()
    assert corpo == {"id": tarefa["id"], "titulo": tarefa["titulo"], "concluida": True}
    assert cliente.get("/tarefas").json()[0]["concluida"] is True


def test_ca13_repetir_conclusao_e_idempotente(cliente):
    tarefa = _cadastrar(cliente)
    primeira = cliente.patch(f"/tarefas/{tarefa['id']}", json={"concluida": True})
    segunda = cliente.patch(f"/tarefas/{tarefa['id']}", json={"concluida": True})
    assert primeira.status_code == 200 and segunda.status_code == 200
    assert primeira.json() == segunda.json()
    assert len(cliente.get("/tarefas").json()) == 1


@pytest.mark.parametrize(
    "corpo", [{}, {"concluida": False}, {"concluida": None}, {"concluida": 1}, {"concluida": 0},
              {"concluida": "true"}, {"concluida": "false"}, {"concluida": [True]},
              {"concluida": {"v": True}}]
)
def test_ca14_corpo_de_conclusao_invalido(cliente, corpo):
    tarefa = _cadastrar(cliente)
    resposta = cliente.patch(f"/tarefas/{tarefa['id']}", json=corpo)
    assert resposta.status_code == 422
    assert cliente.get("/tarefas").json()[0] == tarefa


def test_ca14_corpo_ausente_ou_malformado(cliente):
    tarefa = _cadastrar(cliente)
    sem_corpo = cliente.patch(f"/tarefas/{tarefa['id']}")
    assert sem_corpo.status_code == 422
    malformado = cliente.patch(
        f"/tarefas/{tarefa['id']}",
        content=b'{"concluida": true',
        headers={"Content-Type": "application/json"},
    )
    assert malformado.status_code == 422
    assert cliente.get("/tarefas").json()[0] == tarefa


@pytest.mark.parametrize("campo_extra", ["id", "prioridade"])
def test_ca15_alteracoes_fora_do_escopo(cliente, campo_extra):
    tarefa = _cadastrar(cliente)
    resposta = cliente.patch(
        f"/tarefas/{tarefa['id']}", json={"concluida": True, campo_extra: 1}
    )
    assert resposta.status_code == 422
    assert cliente.get("/tarefas").json()[0] == tarefa


def test_ca16_concluir_id_inexistente(cliente):
    resposta = cliente.patch("/tarefas/999", json={"concluida": True})
    assert resposta.status_code == 404
    assert resposta.json() == {"detail": MENSAGEM_NAO_ENCONTRADA}


@pytest.mark.parametrize("corpo", [
    {"concluida": False},
    {"titulo": ""},
    {"titulo": "", "concluida": True},
    {"titulo": "Válido", "concluida": False},
])
def test_ca17_validacao_de_entrada_antes_da_consulta(cliente, corpo):
    resposta = cliente.patch("/tarefas/999", json=corpo)
    assert resposta.status_code == 422
    assert cliente.get("/tarefas").json() == []


# ------------------------------------------------------------ Exclusão/IDs

@pytest.mark.parametrize("concluida", [False, True], ids=["pendente", "concluida"])
def test_ca18_exclusao(cliente, concluida):
    tarefa = _cadastrar(cliente)
    if concluida:
        resposta = cliente.patch(f"/tarefas/{tarefa['id']}", json={"concluida": True})
        assert resposta.status_code == 200
        assert resposta.json()["concluida"] is True

    resposta = cliente.delete(f"/tarefas/{tarefa['id']}")
    assert resposta.status_code == 204
    assert resposta.content == b""
    assert cliente.get("/tarefas").json() == []


def test_ca19_exclusao_de_id_inexistente(cliente):
    outra = _cadastrar(cliente, "Preservar")
    resposta = cliente.delete(f"/tarefas/{outra['id'] + 1}")
    assert resposta.status_code == 404
    assert resposta.json() == {"detail": MENSAGEM_NAO_ENCONTRADA}
    assert cliente.get("/tarefas").json() == [outra]


def test_ca20_repetir_exclusao(cliente):
    tarefa = _cadastrar(cliente)
    primeira = cliente.delete(f"/tarefas/{tarefa['id']}")
    segunda = cliente.delete(f"/tarefas/{tarefa['id']}")
    assert primeira.status_code == 204
    assert segunda.status_code == 404
    assert cliente.get("/tarefas").json() == []


@pytest.mark.parametrize("id_invalido", ["abc", "1.5", "0", "-1", str(ID_MAXIMO + 1)])
def test_ca21_id_invalido(cliente, id_invalido):
    tarefa = _cadastrar(cliente)
    respostas = [
        cliente.patch(f"/tarefas/{id_invalido}", json={"concluida": True}),
        cliente.delete(f"/tarefas/{id_invalido}"),
    ]
    for resposta in respostas:
        assert resposta.status_code == 422
        assert any(erro["loc"] == ["path", "id"] for erro in resposta.json()["detail"])
    assert cliente.get("/tarefas").json() == [tarefa]


def test_ca22_limite_valido_de_id(cliente):
    assert cliente.patch(f"/tarefas/{ID_MAXIMO}", json={"concluida": True}).status_code == 404
    assert cliente.delete(f"/tarefas/{ID_MAXIMO}").status_code == 404


# ------------------------------------------------ Persistência e contrato

def test_ca25_formato_das_respostas(cliente):
    criada = cliente.post("/tarefas", json={"titulo": "Estudar"})
    assert criada.status_code == 201
    tarefa_id = criada.json()["id"]
    listagem = cliente.get("/tarefas")
    atualizada = cliente.patch(f"/tarefas/{tarefa_id}", json={"concluida": True})
    assert listagem.status_code == atualizada.status_code == 200

    sem_conteudo = cliente.delete(f"/tarefas/{tarefa_id}")
    assert sem_conteudo.status_code == 204
    assert sem_conteudo.content == b""

    ausente = cliente.delete(f"/tarefas/{tarefa_id}")
    assert ausente.status_code == 404
    erro = cliente.post("/tarefas", json={})
    assert erro.status_code == 422

    for resposta in (criada, listagem, atualizada, ausente, erro):
        assert resposta.headers["content-type"].startswith("application/json")
        assert isinstance(resposta.json(), (dict, list))

    detalhe = erro.json()["detail"]
    assert isinstance(detalhe, list) and len(detalhe) >= 1
    for item in detalhe:
        assert {"loc", "msg", "type"} <= item.keys()


# --------------------------------------------------------------- Edição

def test_ca27_editar_tarefa_pendente(cliente):
    tarefa = _cadastrar(cliente, "Estudar matematca")
    outra = _cadastrar(cliente, "Preservar")
    resposta = cliente.patch(f"/tarefas/{tarefa['id']}", json={"titulo": "Estudar matemática"})
    assert resposta.status_code == 200
    corpo = resposta.json()
    assert corpo == {"id": tarefa["id"], "titulo": "Estudar matemática", "concluida": False}
    assert cliente.get("/tarefas").json() == [corpo, outra]

    repetida = cliente.patch(f"/tarefas/{tarefa['id']}", json={"titulo": "Estudar matemática"})
    assert repetida.status_code == 200
    assert repetida.json() == corpo
    substituida = cliente.patch(f"/tarefas/{tarefa['id']}", json={"titulo": "Revisar português"})
    assert substituida.status_code == 200
    assert substituida.json() == {**corpo, "titulo": "Revisar português"}
    assert cliente.get("/tarefas").json() == [substituida.json(), outra]


def test_ca28_editar_tarefa_concluida_nao_reabre(cliente):
    tarefa = _cadastrar(cliente, "Estudar")
    assert cliente.patch(f"/tarefas/{tarefa['id']}", json={"concluida": True}).status_code == 200
    resposta = cliente.patch(f"/tarefas/{tarefa['id']}", json={"titulo": "Revisar"})
    assert resposta.status_code == 200
    assert resposta.json() == {"id": tarefa["id"], "titulo": "Revisar", "concluida": True}
    assert cliente.get("/tarefas").json() == [resposta.json()]


def test_ca29_validar_titulo_na_edicao(cliente):
    tarefa = _cadastrar(cliente)
    outra = _cadastrar(cliente, "Já existe")

    assert cliente.patch(f"/tarefas/{tarefa['id']}", json={"titulo": "a" * 120}).status_code == 200
    antes = cliente.get("/tarefas").json()
    assert cliente.patch(f"/tarefas/{tarefa['id']}", json={"titulo": "a" * 121}).status_code == 422
    assert cliente.get("/tarefas").json() == antes
    # Título já usado por outra tarefa é permitido (RN-03).
    permitido = cliente.patch(f"/tarefas/{tarefa['id']}", json={"titulo": outra["titulo"]})
    assert permitido.status_code == 200
    assert permitido.json() == {**tarefa, "titulo": outra["titulo"]}
    assert cliente.get("/tarefas").json() == [permitido.json(), outra]


@pytest.mark.parametrize("titulo", [
    "a", "á" * 120, "  Revisar  português  ", "  " + "á" * 120 + "  ",
], ids=["minimo", "limite-unicode", "espacos-e-acentos", "limite-com-espacos"])
def test_ca29_normalizacao_e_limites_na_edicao(cliente, titulo):
    tarefa = _cadastrar(cliente)
    resposta = cliente.patch(f"/tarefas/{tarefa['id']}", json={"titulo": titulo})
    assert resposta.status_code == 200
    assert resposta.json() == {**tarefa, "titulo": titulo.strip()}
    assert cliente.get("/tarefas").json() == [resposta.json()]


@pytest.mark.parametrize("titulo", [
    "", "   ", "\t\n", "á" * 121, "  " + "a" * 121 + "  ",
    None, 1, True, ["a"], {"a": 1},
], ids=["vazio", "espacos", "tabulacao", "longo-unicode", "longo-com-espacos",
        "nulo", "numero", "booleano", "lista", "objeto"])
def test_ca29_rejeita_titulo_invalido_na_edicao(cliente, titulo):
    tarefa = _cadastrar(cliente)
    resposta = cliente.patch(f"/tarefas/{tarefa['id']}", json={"titulo": titulo})
    assert resposta.status_code == 422
    assert cliente.get("/tarefas").json()[0] == tarefa


def test_ca30_editar_e_concluir_juntos(cliente):
    tarefa = _cadastrar(cliente, "Estudar")
    resposta = cliente.patch(
        f"/tarefas/{tarefa['id']}", json={"titulo": "Revisar português", "concluida": True}
    )
    assert resposta.status_code == 200
    assert resposta.json() == {
        "id": tarefa["id"], "titulo": "Revisar português", "concluida": True,
    }
    assert cliente.get("/tarefas").json() == [resposta.json()]


@pytest.mark.parametrize(
    "corpo",
    [{"titulo": "", "concluida": True}, {"titulo": "Válido", "concluida": False}],
)
def test_ca30_combinacao_com_um_campo_invalido_nao_altera_nada(cliente, corpo):
    tarefa = _cadastrar(cliente, "Original")
    resposta = cliente.patch(f"/tarefas/{tarefa['id']}", json=corpo)
    assert resposta.status_code == 422
    assert cliente.get("/tarefas").json()[0] == tarefa


def test_ca31_editar_id_inexistente(cliente):
    outra = _cadastrar(cliente, "Preservar")
    resposta = cliente.patch(f"/tarefas/{outra['id'] + 1}", json={"titulo": "Novo título"})
    assert resposta.status_code == 404
    assert resposta.json() == {"detail": MENSAGEM_NAO_ENCONTRADA}
    assert cliente.get("/tarefas").json() == [outra]


# --------------------------------------------------- Persistência (RF-07)

def test_rf07_persistencia_entre_reinicializacoes(tmp_path):
    """CA-23: dois processos carregam a API com o mesmo arquivo SQLite."""
    caminho_banco = tmp_path / "persistencia.db"
    ambiente = {
        **os.environ,
        "TAREFAS_DATABASE_URL": f"sqlite:///{caminho_banco}",
        "PYTHONIOENCODING": "utf-8",
    }

    def executar(codigo):
        resultado = subprocess.run(
            [sys.executable, "-c", textwrap.dedent(codigo)],
            cwd=Path(__file__).resolve().parents[1],
            env=ambiente, capture_output=True, text=True, encoding="utf-8", timeout=30,
        )
        assert resultado.returncode == 0, resultado.stdout + resultado.stderr
        return json.loads(resultado.stdout)

    try:
        esperadas = executar("""
            import json
            from fastapi.testclient import TestClient
            from app.main import app
            from app.database import engine

            try:
                with TestClient(app) as cliente:
                    tarefas = []
                    for titulo in ("Editar", "Concluir", "Excluir"):
                        resposta = cliente.post("/tarefas", json={"titulo": titulo})
                        assert resposta.status_code == 201
                        tarefas.append(resposta.json())
                    a, b, c = tarefas
                    editada = cliente.patch(f"/tarefas/{a['id']}", json={"titulo": "Editada"})
                    concluida = cliente.patch(f"/tarefas/{b['id']}", json={"concluida": True})
                    excluida = cliente.delete(f"/tarefas/{c['id']}")
                    assert editada.status_code == concluida.status_code == 200
                    assert excluida.status_code == 204
                    esperadas = [
                        {**a, "titulo": "Editada"},
                        {**b, "concluida": True},
                    ]
                    assert cliente.get("/tarefas").json() == esperadas
                    print(json.dumps(esperadas))
            finally:
                engine.dispose()
        """)
        obtidas = executar("""
            import json
            from fastapi.testclient import TestClient
            from app.main import app
            from app.database import engine

            try:
                with TestClient(app) as cliente:
                    resposta = cliente.get("/tarefas")
                    assert resposta.status_code == 200
                    print(json.dumps(resposta.json()))
            finally:
                engine.dispose()
        """)
        assert obtidas == esperadas
    finally:
        caminho_banco.unlink(missing_ok=True)
