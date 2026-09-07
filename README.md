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
O `PATCH /tarefas/{id}` permite editar `titulo`, enviar `concluida: true` ou ambos,
preservando o ID e os campos omitidos. O projeto mantém quatro operações HTTP.

## Fluxo de trabalho

O projeto utiliza Issues, GitHub Projects, branches de funcionalidade e Pull Requests. Cada alteração deve seguir o fluxo:

```text
Issue → branch → commits → Pull Request → revisão → testes → merge
```

## Especificação e decisões técnicas

A proposta técnica da entrega inicial usa Python 3.12, FastAPI, Pydantic 2,
SQLAlchemy 2 e SQLite. A aplicação terá uma única tabela e acesso síncrono ao
banco. pytest e TestClient apoiarão a validação; Docker e GitHub Actions serão
configurados nas tarefas de ambiente e CI. Essas escolhas priorizam facilidade
de execução, escopo pequeno e aderência ao roteiro.

- [Especificação SDD](docs/especificacao_sdd.md): requisitos, regras e contratos.
- [Decisões técnicas e arquitetura](docs/decisoes_tecnicas.md): justificativas e ADRs.
- [Contrato OpenAPI](docs/openapi.json): definição das quatro operações em formato estruturado.
- [Critérios de aceitação](docs/criterios_aceitacao.md): cenários para implementação e testes.
- [Registro de refinamentos](docs/refinamentos.md): decisões iniciais e acompanhamento da revisão.
- [Guia da minha contribuição](docs/entrega_vitor.md): escopo, dependências e checklist de revisão.

Preparei estes documentos para a [Issue #1](https://github.com/gabrielavieirab/tarefas-api/issues/1).
Minha proposta está pendente de revisão por Felipe e Caike. Os comandos de execução
e as evidências da aplicação serão consolidados conforme a implementação, o ambiente e os testes
forem integrados.
