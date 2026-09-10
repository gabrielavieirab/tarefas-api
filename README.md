# API de Gerenciamento de Tarefas

API REST simples para criação, consulta, atualização e exclusão de tarefas. O projeto foi desenvolvido como parte do Bootcamp e utiliza Python, FastAPI, SQLite, SQLAlchemy, pytest, Docker e GitHub Actions.

## Status do projeto

A implementação principal da API, os testes automatizados, o ambiente Docker e o pipeline de integração contínua já foram integrados à branch `develop`.

Durante a validação manual, foi identificada uma inconsistência no identificador da primeira tarefa: o `POST /tarefas` e o `GET /tarefas` retornam `id: 0`, enquanto `PATCH /tarefas/{id}` e `DELETE /tarefas/{id}` exigem valores a partir de `1`. A correção está pendente de integração e a validação funcional final será repetida após esse ajuste.

## Objetivo

Disponibilizar uma API pequena e objetiva para gerenciar tarefas, permitindo registrar uma tarefa, consultar tarefas existentes, atualizar seus dados e removê-la.

## Equipe

| Integrante | Responsabilidade | RA |
|---|---|---|
| Vitor de Assis Patricio Borges | Especificação SDD, contratos e decisões técnicas | 22304737 |
| Gabriela Vieira Baptista | GitHub, organização, documentação e evidências | 22510133 |
| Felipe Domingos Ribeiro Pereira | Implementação da API e banco de dados | 22604250 |
| Caike Ribeiro Menezes | Testes, Docker e GitHub Actions | 22601978 |

## Tecnologias

- Python 3.12
- FastAPI
- Uvicorn
- SQLite
- SQLAlchemy
- Pydantic
- pytest
- Docker
- GitHub Actions

## Funcionalidades

A API possui as seguintes operações:

| Método | Rota | Descrição |
|---|---|---|
| `POST` | `/tarefas` | Cria uma nova tarefa. |
| `GET` | `/tarefas` | Lista as tarefas cadastradas. |
| `PATCH` | `/tarefas/{id}` | Atualiza uma tarefa existente. |
| `DELETE` | `/tarefas/{id}` | Exclui uma tarefa existente. |

Cada tarefa possui, no mínimo, os campos:

```json
{
  "id": 1,
  "titulo": "Estudar a API",
  "concluida": false
}
