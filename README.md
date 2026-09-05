# tarefas-api

API de lista de tarefas com cadastro, listagem, conclusão e exclusão.

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
