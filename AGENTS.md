# Diretrizes do projeto

## Contexto
Este projeto é uma API simples de gerenciamento de tarefas desenvolvida em Python com FastAPI, SQLite, SQLAlchemy e pytest.

## Funcionalidades obrigatórias
- POST /tarefas: criar tarefa.
- GET /tarefas: listar tarefas.
- PATCH /tarefas/{id}: marcar tarefa como concluída.
- DELETE /tarefas/{id}: excluir tarefa.

## Modelo
Cada tarefa possui id, titulo e concluida.

## Regras
- titulo é obrigatório e não pode ser vazio.
- Uma nova tarefa começa com concluida=false.
- ID inexistente deve retornar 404.
- Entrada inválida deve retornar 422.
- Não criar funcionalidades fora do escopo sem atualizar a especificação.

## Regras para alterações
- Toda mudança de comportamento deve incluir testes.
- Ler docs/especificacao_sdd.md antes de implementar.
- Executar pytest antes de abrir Pull Request.
- Não remover testes para fazer a suíte passar.
- Revisar o diff antes de enviar alterações.

## Comandos
python -m pip install -e ".[test]"
pytest
uvicorn app.main:app --reload
