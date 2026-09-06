# API de Gerenciamento de Tarefas

## Objetivo

Esta é uma API simples para gerenciamento de tarefas. O sistema permite criar, listar, atualizar e excluir tarefas por meio de quatro operações HTTP.

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
- SQLite
- SQLAlchemy
- pytest
- Docker

## Operações da API

| Método | Rota | Descrição |
|---|---|---|
| POST | `/tarefas` | Cadastrar uma tarefa. |
| GET | `/tarefas` | Listar as tarefas cadastradas. |
| PATCH | `/tarefas/{id}` | Atualizar uma tarefa ou marcá-la como concluída. |
| DELETE | `/tarefas/{id}` | Excluir uma tarefa. |

Cada tarefa possui os campos `id`, `titulo` e `concluida`.

## Fluxo de trabalho

O projeto utiliza Issues, GitHub Projects, branches de funcionalidade e Pull Requests. Cada alteração deve seguir o fluxo:

```text
Issue → branch → commits → Pull Request → revisão → testes → merge
