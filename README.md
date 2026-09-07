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

## Instalação e execução

Use Python 3.12. A validação desta contribuição usa Python 3.12.10.
Na raiz do repositório, crie e ative um ambiente virtual.

Windows (PowerShell):

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Linux/macOS:

```bash
python3.12 -m venv .venv
source .venv/bin/activate
```

Com o ambiente ativo:

```bash
python -m pip install -e ".[test]"
python -m pip check
python -m uvicorn app.main:app --reload
```

A API atende em http://127.0.0.1:8000 e a documentação interativa em
http://127.0.0.1:8000/docs. O banco e a tabela são criados na inicialização.
Por padrão, o arquivo é `tarefas.db` no diretório de execução.

Para escolher outro banco, defina `TAREFAS_DATABASE_URL` **antes** de iniciar
a aplicação. Exemplo no PowerShell:

```powershell
$env:TAREFAS_DATABASE_URL = "sqlite:///./outro_banco.db"
python -m uvicorn app.main:app --reload
```

No Linux/macOS, use `export TAREFAS_DATABASE_URL="sqlite:///./outro_banco.db"`.
O diretório escolhido deve existir.

## Testes

```bash
python -m pytest -v
```

A suíte aproveita os testes de modelo e das rotas existentes, complementando os
CA-01 a CA-31. Cada teste recebe seu próprio SQLite temporário. A inicialização
da API também usa um banco separado, e os arquivos são removidos após fechar as
conexões. Não é necessário criar ou apagar o banco manual para executar testes.

O teste de reinicialização abre a aplicação em dois processos com o mesmo arquivo
temporário. O teste de isolamento verifica que a suíte não abre o banco manual e
restaura a variável de ambiente e as dependências do FastAPI.

As dependências diretas estão fixadas no `pyproject.toml`. Por decisão desta etapa,
não foi criado constraints/lock; as versões transitivas ainda podem variar.
Consulte [as evidências](docs/evidencias_testes.md) para o resultado e as limitações
da validação, incluindo o que falta para concluir o CA-26.

## Docker

Com o Docker em execução:

```bash
docker build -t tarefas-api:test .
docker run --rm tarefas-api:test python -m pytest -v
docker run --rm -p 8000:8000 -v tarefas-dados:/data tarefas-api:test
```

A imagem usa Python 3.12.10 e instala o mesmo extra `[test]`.
A API grava em `/data/tarefas.db`; o volume `tarefas-dados` preserva os dados
quando o container é recriado. Os testes usam arquivos temporários próprios.
Para parar a API executada em primeiro plano, pressione Ctrl+C.

## Integração contínua

O workflow [tests.yml](.github/workflows/tests.yml) executa em Pull Requests
destinados a `develop` ou `main` e em pushes nessas duas branches.
Ele instala as dependências, confere o ambiente, executa pytest, constrói a imagem
e executa a mesma suíte no container. Uma falha impede o sucesso do job.

Os logs registram o commit, o Python, as dependências e os resultados.
Os relatórios XML ficam no artefato `resultados-testes` da execução no GitHub Actions.
O workflow não faz deploy nem merge. A configuração só terá evidência remota
depois de enviada e executada no GitHub.
