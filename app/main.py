"""Cria a aplicação FastAPI, inicializa o banco e registra as rotas
(decomposição em componentes de docs/decisoes_tecnicas.md).
"""
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.database import init_db
from app.routes import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()  # cria a tabela no banco de uso manual, se ainda não existir.
    yield


app = FastAPI(
    title="API de lista de tarefas",
    version="1.1.0",
    description=(
        "Quatro operações HTTP (POST, GET, PATCH, DELETE) sobre uma lista "
        "compartilhada de tarefas. Ver docs/especificacao_sdd.md."
    ),
    lifespan=lifespan,
)

app.include_router(router)
