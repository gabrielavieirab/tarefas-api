# API de Gerenciamento de Tarefas

API REST simples para criação, consulta, atualização e exclusão de tarefas. O projeto foi desenvolvido como parte do Bootcamp com Python, FastAPI, SQLite, SQLAlchemy, pytest, Docker e GitHub Actions.

## Status do projeto

A implementação principal da API, os testes automatizados, o ambiente Docker, o pipeline de integração contínua e a documentação estão organizados no repositório e integrados ao fluxo de desenvolvimento.

Durante a validação manual inicial, foi identificada uma diferença entre versões relacionadas ao identificador da primeira tarefa. A equipe está confirmando o comportamento na versão mais recente da branch `develop` antes da validação funcional final.

## Objetivo

Disponibilizar uma API pequena e objetiva para gerenciar tarefas, permitindo registrar uma tarefa, consultar tarefas existentes, atualizar seus dados e removê-la.

## Equipe

| Integrante | Responsabilidade | RA |
|---|---|---|
| Vitor de Assis Patricio Borges | Especificação e decisões técnicas | 22304737 |
| Gabriela Vieira Baptista | GitHub, agente de IA e documentação final | 22510133 |
| Felipe Domingos Ribeiro Pereira | Implementação e banco de dados | 22604250 |
| Caike Ribeiro Menezes | Ambiente, testes e integração contínua | 22601978 |

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

| Método | Rota | Descrição |
|---|---|---|
| `POST` | `/tarefas` | Cria uma nova tarefa. |
| `GET` | `/tarefas` | Lista as tarefas cadastradas. |
| `PATCH` | `/tarefas/{id}` | Atualiza uma tarefa existente. |
| `DELETE` | `/tarefas/{id}` | Exclui uma tarefa existente. |

Cada tarefa possui os campos `id`, `titulo` e `concluida`.

Exemplo:

```json
{
  "id": 1,
  "titulo": "Estudar a API",
  "concluida": false
}
