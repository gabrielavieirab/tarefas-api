"""Testes da camada de banco de dados (app/database.py e app/models.py).

Cobrem, no nível do banco: RN-01 (tarefa nasce pendente), a obrigatoriedade do título
(seção 6 da especificação) e a persistência em arquivo entre conexões
(RF-07/RN-11). Cada teste usa um arquivo SQLite temporário isolado,
conforme a ADR-004 (banco limpo por teste, arquivo temporário em vez de
memória compartilhada).
"""
import pytest
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker

from app.database import criar_engine, init_db
from app.models import Tarefa


@pytest.fixture
def sessao(tmp_path):
    caminho_banco = tmp_path / "teste_tarefas.db"
    engine = criar_engine(f"sqlite:///{caminho_banco}")
    Sessao = sessionmaker(bind=engine)
    sessao = Sessao()
    try:
        init_db(engine)
        yield sessao
    finally:
        sessao.close()
        engine.dispose()
        caminho_banco.unlink(missing_ok=True)


def test_tarefa_nasce_pendente_com_id_gerado(sessao):
    tarefa = Tarefa(titulo="Estudar")
    sessao.add(tarefa)
    sessao.commit()

    assert tarefa.id is not None
    assert tarefa.id > 0
    assert tarefa.concluida is False


def test_titulo_e_obrigatorio_nao_nulo(sessao):
    tarefa = Tarefa(titulo=None)
    sessao.add(tarefa)

    with pytest.raises(IntegrityError):
        sessao.commit()


def test_ids_crescem_a_cada_cadastro(sessao):
    primeira = Tarefa(titulo="Primeira")
    sessao.add(primeira)
    sessao.commit()

    segunda = Tarefa(titulo="Segunda")
    sessao.add(segunda)
    sessao.commit()

    assert segunda.id > primeira.id


def test_registros_persistem_entre_conexoes(tmp_path):
    caminho_banco = tmp_path / "persistencia.db"
    url = f"sqlite:///{caminho_banco}"

    engine_1 = criar_engine(url)
    engine_2 = criar_engine(url)
    try:
        init_db(engine_1)
        with sessionmaker(bind=engine_1)() as sessao_1:
            sessao_1.add(Tarefa(titulo="Sobrevive ao reinicio"))
            sessao_1.commit()
        engine_1.dispose()

        with sessionmaker(bind=engine_2)() as sessao_2:
            tarefas = sessao_2.query(Tarefa).all()
            assert len(tarefas) == 1
            assert tarefas[0].titulo == "Sobrevive ao reinicio"
    finally:
        engine_1.dispose()
        engine_2.dispose()
        caminho_banco.unlink(missing_ok=True)
