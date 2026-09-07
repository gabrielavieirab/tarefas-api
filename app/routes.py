"""As quatro operações HTTP da API (seção 8 de docs/especificacao_sdd.md).

Valida ID e corpo pelos esquemas (Pydantic/FastAPI cuidam disso antes desta
camada ser chamada, o que já garante a ordem exigida pela RN-09: entrada
inválida vira 422 mesmo com ID inexistente). Esta camada só traduz "registro
ausente" em HTTP 404, mantendo os detalhes HTTP fora do módulo de
persistência (ADR-002).
"""
from fastapi import APIRouter, Depends, HTTPException, Path, status
from sqlalchemy.orm import Session

from app import crud
from app.database import get_db
from app.schemas import TarefaAtualizar, TarefaCreate, TarefaRead

router = APIRouter(tags=["Tarefas"])

# Inteiro positivo até o limite de 64 bits assinado (RN-08 / seção 6).
_ID_TAREFA = Path(
    ...,
    ge=1,
    le=9_223_372_036_854_775_807,
    description="Inteiro positivo de 64 bits.",
)

_TAREFA_NAO_ENCONTRADA = "Tarefa não encontrada."


@router.post(
    "/tarefas",
    response_model=TarefaRead,
    status_code=status.HTTP_201_CREATED,
    summary="Cadastrar uma tarefa pendente",
)
def criar_tarefa(dados: TarefaCreate, sessao: Session = Depends(get_db)) -> TarefaRead:
    return crud.criar_tarefa(sessao, dados.titulo)


@router.get(
    "/tarefas",
    response_model=list[TarefaRead],
    summary="Listar todas as tarefas",
)
def listar_tarefas(sessao: Session = Depends(get_db)) -> list[TarefaRead]:
    return crud.listar_tarefas(sessao)


@router.patch(
    "/tarefas/{id}",
    response_model=TarefaRead,
    summary="Editar o texto e/ou concluir uma tarefa",
)
def atualizar_tarefa(
    dados: TarefaAtualizar,
    id: int = _ID_TAREFA,
    sessao: Session = Depends(get_db),
) -> TarefaRead:
    alteracoes = dados.model_dump(exclude_unset=True)
    tarefa = crud.atualizar_tarefa(sessao, id, alteracoes)
    if tarefa is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=_TAREFA_NAO_ENCONTRADA)
    return tarefa


@router.delete(
    "/tarefas/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Excluir uma tarefa",
)
def excluir_tarefa(id: int = _ID_TAREFA, sessao: Session = Depends(get_db)) -> None:
    se_excluiu = crud.excluir_tarefa(sessao, id)
    if not se_excluiu:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=_TAREFA_NAO_ENCONTRADA)
