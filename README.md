# API de Gerenciamento de Tarefas

API REST simples para criação, consulta, atualização e exclusão de tarefas. O projeto foi desenvolvido como parte do Bootcamp com Python, FastAPI, SQLite, SQLAlchemy, Pydantic, pytest, Docker e GitHub Actions.

## Visão geral

O sistema permite gerenciar tarefas por meio de quatro operações HTTP. Cada tarefa possui um identificador, um título e um status de conclusão. A API foi organizada para ser simples, testável e fácil de executar em diferentes ambientes.

## Status do projeto

A implementação principal da API, os testes automatizados, o ambiente Docker, o pipeline de integração contínua e a documentação estão organizados no repositório e integrados ao fluxo de desenvolvimento.

A validação funcional foi concluída com sucesso. Confirmou-se que o banco de dados gera os identificadores automaticamente a partir de 1 e que o endpoint GET retorna corretamente os IDs persistidos. A suíte automatizada foi executada com 80 testes aprovados.

## Objetivo

Disponibilizar uma API pequena e objetiva para gerenciar tarefas, permitindo registrar uma tarefa, consultar tarefas existentes, atualizar seus dados ou status de conclusão e removê-la.

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

## Funcionalidades e rotas

| Método | Rota | Descrição |
|---|---|---|
| `POST` | `/tarefas` | Cria uma nova tarefa. |
| `GET` | `/tarefas` | Lista as tarefas cadastradas. |
| `PATCH` | `/tarefas/{id}` | Atualiza uma tarefa existente ou altera seu status. |
| `DELETE` | `/tarefas/{id}` | Exclui uma tarefa existente. |

Cada tarefa possui os campos `id`, `titulo` e `concluida`.

Exemplo de tarefa:

```json
{
  "id": 1,
  "titulo": "Estudar a API",
  "concluida": false
}
