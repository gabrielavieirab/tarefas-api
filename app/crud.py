"""Operações de persistência sobre a tabela `tarefas` (ADR-002).

Cada função recebe uma sessão já aberta (uma por requisição, via
`app.database.get_db`) e confirma a escrita antes de retornar sucesso
(RNF-05). A tradução de "registro ausente" para HTTP 404 é responsabilidade
da camada de rotas, não deste módulo (ver decomposição em componentes de
docs/decisoes_tecnicas.md).
"""
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Tarefa


def criar_tarefa(sessao: Session, titulo: str) -> Tarefa:
    """Persiste uma tarefa nova, pendente (RN-01). `titulo` já validado."""
    tarefa = Tarefa(titulo=titulo)
    sessao.add(tarefa)
    try:
        sessao.commit()
    except Exception:
        sessao.rollback()
        raise
    sessao.refresh(tarefa)
    return tarefa


def listar_tarefas(sessao: Session) -> list[Tarefa]:
    """Retorna todas as tarefas em ordem crescente de ID (RN-10)."""
    return list(sessao.execute(select(Tarefa).order_by(Tarefa.id.asc())).scalars().all())


def buscar_tarefa(sessao: Session, tarefa_id: int) -> Tarefa | None:
    """Busca uma tarefa pelo ID; `None` se não existir."""
    return sessao.get(Tarefa, tarefa_id)


def atualizar_tarefa(sessao: Session, tarefa_id: int, alteracoes: dict) -> Tarefa | None:
    """Aplica só os campos presentes em `alteracoes` (já validados) e
    preserva os demais (RN-12). Retorna a tarefa atualizada ou `None` se o
    ID não existir; não cria registro novo.
    """
    tarefa = buscar_tarefa(sessao, tarefa_id)
    if tarefa is None:
        return None
    for campo, valor in alteracoes.items():
        setattr(tarefa, campo, valor)
    try:
        sessao.commit()
    except Exception:
        sessao.rollback()
        raise
    sessao.refresh(tarefa)
    return tarefa


def excluir_tarefa(sessao: Session, tarefa_id: int) -> bool:
    """Remove a tarefa do banco. Retorna `True` se havia registro (RN-07)."""
    tarefa = buscar_tarefa(sessao, tarefa_id)
    if tarefa is None:
        return False
    sessao.delete(tarefa)
    try:
        sessao.commit()
    except Exception:
        sessao.rollback()
        raise
    return True
