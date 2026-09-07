"""Cenários de aceitação da API (docs/criterios_aceitacao.md, CA-01 a CA-31).

Cada teste referencia o(s) critério(s)/regra(s) que cobre. Usa a fixture
`cliente` (tests/conftest.py): banco SQLite temporário e limpo por teste.
"""
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


def test_ca02_normalizacao_do_titulo(cliente):
    resposta = cliente.post("/tarefas", json={"titulo": "  Revisar  API  "})
    assert resposta.status_code == 201
    # Remove só as extremidades; espaços internos e acentos são preservados.
    assert resposta.json()["titulo"] == "Revisar  API"


@pytest.mark.parametrize("titulo", ["", "   ", "\t\n"])
def test_ca03_titulo_ausente_ou_vazio(cliente, titulo):
    resposta = cliente.post("/tarefas", json={"titulo": titulo})
    assert resposta.status_code == 422
    assert cliente.get("/tarefas").json() == []


def test_ca03_titulo_ausente_do_corpo(cliente):
    resposta = cliente.post("/tarefas", json={})
    assert resposta.status_code == 422
    assert cliente.get("/tarefas").json() == []


@pytest.mark.parametrize("titulo", [None, 123, True, ["a"], {"x": 1}])
def test_ca04_tipo_invalido_de_titulo(cliente, titulo):
    resposta = cliente.post("/tarefas", json={"titulo": titulo})
    assert resposta.status_code == 422
    assert cliente.get("/tarefas").json() == []


def test_ca05_limites_do_titulo(cliente):
    titulo_120 = "a" * 120
    assert cliente.post("/tarefas", json={"titulo": titulo_120}).status_code == 201

    titulo_121 = "a" * 121
    assert cliente.post("/tarefas", json={"titulo": titulo_121}).status_code == 422

    # 120 caracteres cercados de espaços: só os 120 são persistidos.
    resposta = cliente.post("/tarefas", json={"titulo": f"  {titulo_120}  "})
    assert resposta.status_code == 201
    assert resposta.json()["titulo"] == titulo_120


@pytest.mark.parametrize("campo_extra", ["id", "concluida", "prioridade"])
def test_ca06_campos_controlados_pelo_servidor(cliente, campo_extra):
    corpo = {"titulo": "Estudar", campo_extra: 1}
    resposta = cliente.post("/tarefas", json=corpo)
    assert resposta.status_code == 422
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
    cliente.patch(f"/tarefas/{t1['id']}", json={"concluida": True})

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
    "corpo", [{}, {"concluida": False}, {"concluida": None}, {"concluida": 1},
              {"concluida": "true"}, {"concluida": "false"}, {"concluida": [True]},
              {"concluida": {"v": True}}]
)
def test_ca14_corpo_de_conclusao_invalido(cliente, corpo):
    tarefa = _cadastrar(cliente)
    resposta = cliente.patch(f"/tarefas/{tarefa['id']}", json=corpo)
    assert resposta.status_code == 422
    assert cliente.get(f"/tarefas").json()[0] == tarefa


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


def test_ca17_validacao_de_entrada_antes_da_consulta(cliente):
    # ID válido e inexistente + corpo inválido: 422, não 404 (RN-09).
    resposta = cliente.patch("/tarefas/999", json={"concluida": False})
    assert resposta.status_code == 422


# ------------------------------------------------------------ Exclusão/IDs

def test_ca18_exclusao(cliente):
    pendente = _cadastrar(cliente, "Pendente")
    concluida = _cadastrar(cliente, "Concluída")
    cliente.patch(f"/tarefas/{concluida['id']}", json={"concluida": True})

    for tarefa in (pendente, concluida):
        resposta = cliente.delete(f"/tarefas/{tarefa['id']}")
        assert resposta.status_code == 204
        assert resposta.content == b""

    assert cliente.get("/tarefas").json() == []


def test_ca19_exclusao_de_id_inexistente(cliente):
    outra = _cadastrar(cliente, "Preservar")
    resposta = cliente.delete("/tarefas/999")
    assert resposta.status_code == 404
    assert resposta.json() == {"detail": MENSAGEM_NAO_ENCONTRADA}
    assert cliente.get("/tarefas").json() == [outra]


def test_ca20_repetir_exclusao(cliente):
    tarefa = _cadastrar(cliente)
    primeira = cliente.delete(f"/tarefas/{tarefa['id']}")
    segunda = cliente.delete(f"/tarefas/{tarefa['id']}")
    assert primeira.status_code == 204
    assert segunda.status_code == 404


@pytest.mark.parametrize("id_invalido", ["abc", "1.5", "0", "-1", str(ID_MAXIMO + 1)])
def test_ca21_id_invalido(cliente, id_invalido):
    assert cliente.patch(f"/tarefas/{id_invalido}", json={"concluida": True}).status_code == 422
    assert cliente.delete(f"/tarefas/{id_invalido}").status_code == 422


def test_ca22_limite_valido_de_id(cliente):
    assert cliente.patch(f"/tarefas/{ID_MAXIMO}", json={"concluida": True}).status_code == 404
    assert cliente.delete(f"/tarefas/{ID_MAXIMO}").status_code == 404


# ------------------------------------------------ Persistência e contrato

def test_ca25_formato_das_respostas(cliente):
    criada = cliente.post("/tarefas", json={"titulo": "Estudar"})
    assert criada.headers["content-type"].startswith("application/json")

    excluida_id = criada.json()["id"]
    sem_conteudo = cliente.delete(f"/tarefas/{excluida_id}")
    assert sem_conteudo.content == b""

    erro = cliente.post("/tarefas", json={})
    assert erro.status_code == 422
    detalhe = erro.json()["detail"]
    assert isinstance(detalhe, list) and len(detalhe) >= 1
    for item in detalhe:
        assert {"loc", "msg", "type"} <= item.keys()


# --------------------------------------------------------------- Edição

def test_ca27_editar_tarefa_pendente(cliente):
    tarefa = _cadastrar(cliente, "Estudar matematca")
    resposta = cliente.patch(f"/tarefas/{tarefa['id']}", json={"titulo": "Estudar matemática"})
    assert resposta.status_code == 200
    corpo = resposta.json()
    assert corpo == {"id": tarefa["id"], "titulo": "Estudar matemática", "concluida": False}
    assert cliente.get("/tarefas").json() == [corpo]


def test_ca28_editar_tarefa_concluida_nao_reabre(cliente):
    tarefa = _cadastrar(cliente, "Estudar")
    cliente.patch(f"/tarefas/{tarefa['id']}", json={"concluida": True})
    resposta = cliente.patch(f"/tarefas/{tarefa['id']}", json={"titulo": "Revisar"})
    assert resposta.status_code == 200
    assert resposta.json() == {"id": tarefa["id"], "titulo": "Revisar", "concluida": True}


def test_ca29_validar_titulo_na_edicao(cliente):
    tarefa = _cadastrar(cliente)
    outra = _cadastrar(cliente, "Já existe")

    assert cliente.patch(f"/tarefas/{tarefa['id']}", json={"titulo": "a" * 120}).status_code == 200
    assert cliente.patch(f"/tarefas/{tarefa['id']}", json={"titulo": "a" * 121}).status_code == 422
    # Título já usado por outra tarefa é permitido (RN-03).
    permitido = cliente.patch(f"/tarefas/{tarefa['id']}", json={"titulo": outra["titulo"]})
    assert permitido.status_code == 200


@pytest.mark.parametrize("titulo", ["", "   ", None, 1, True, ["a"], {"a": 1}])
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
    resposta = cliente.patch("/tarefas/999", json={"titulo": "Novo título"})
    assert resposta.status_code == 404
    assert resposta.json() == {"detail": MENSAGEM_NAO_ENCONTRADA}
    assert cliente.get("/tarefas").json() == []


# --------------------------------------------------- Persistência (RF-07)

def test_rf07_persistencia_entre_reinicializacoes(tmp_path):
    """Simula reiniciar a "aplicação": dois engines diferentes, um de cada
    vez, apontando para o mesmo arquivo (sem recriar tabelas na 2ª vez), e
    confirma que os dados sobrevivem (RF-07/RN-11/CA-23).

    Usa um novo engine/sessão por "execução" em vez de recarregar módulos:
    reimportar `app.database` recriaria a classe `Base`, desconectando o
    `Tarefa` já importado dela (mesma armadilha corrigida em
    `app/database.py` para `python -m app.database`).
    """
    from fastapi.testclient import TestClient
    from sqlalchemy.orm import sessionmaker

    from app.database import criar_engine, get_db, init_db
    from app.main import app

    caminho_banco = tmp_path / "persistencia.db"
    url = f"sqlite:///{caminho_banco}"

    def _cliente_para(engine):
        sessao_local = sessionmaker(bind=engine)

        def get_db_local():
            sessao = sessao_local()
            try:
                yield sessao
            finally:
                sessao.close()

        app.dependency_overrides[get_db] = get_db_local
        return TestClient(app)

    engine_1 = criar_engine(url)
    init_db(engine_1)
    with _cliente_para(engine_1) as cliente_1:
        a = cliente_1.post("/tarefas", json={"titulo": "Sobrevive"}).json()
        b = cliente_1.post("/tarefas", json={"titulo": "Editada"}).json()
        c = cliente_1.post("/tarefas", json={"titulo": "Excluída"}).json()
        cliente_1.patch(f"/tarefas/{b['id']}", json={"titulo": "Editada com sucesso"})
        cliente_1.patch(f"/tarefas/{c['id']}", json={"concluida": True})
        cliente_1.delete(f"/tarefas/{c['id']}")
    engine_1.dispose()

    # Nova "execução": engine novo para o mesmo arquivo, sem recriar tabelas.
    engine_2 = criar_engine(url)
    with _cliente_para(engine_2) as cliente_2:
        listagem = cliente_2.get("/tarefas").json()
    engine_2.dispose()
    app.dependency_overrides.clear()

    assert {t["id"] for t in listagem} == {a["id"], b["id"]}
    editada = next(t for t in listagem if t["id"] == b["id"])
    assert editada["titulo"] == "Editada com sucesso"
