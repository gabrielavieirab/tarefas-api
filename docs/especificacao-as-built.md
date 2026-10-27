# Especificação técnica As-Built — Entrega Final

Atualização: **27/10/2026**. Este documento consolida a base documental
integrada pelo [PR #30](https://github.com/gabrielavieirab/tarefas-api/pull/30).

Base conferida: `develop` no commit
[`668faae`](https://github.com/gabrielavieirab/tarefas-api/commit/668faae7bdc54024c1b7c75ca483aa9adfe21d8d).
A consolidação documental está na branch `codex/documentacao-entrega3`.
Descreve o código integrado nessa base; uma mudança posterior exige nova conferência.

## 1. Objetivo, escopo e versões

A API mantém uma lista compartilhada de tarefas, persistida em SQLite. São quatro
operações de negócio: cadastrar, listar, atualizar e excluir. A atualização edita
o título, conclui a tarefa ou aplica ambas as alterações. Cada registro contém
somente `id`, `titulo` e `concluida`.

Não há usuários, autenticação, interface própria, consulta individual por GET,
filtros, paginação, categorias ou reabertura. Swagger e ReDoc apoiam a consulta
ao contrato e não acrescentam operações de negócio.

O contrato continua em **1.1.0**, versão declarada em `app/main.py` e em
`docs/openapi.json`. O pacote em `pyproject.toml` continua em **0.1.0**.
**v1.0.0** é o nome de Release previsto na divisão da Entrega Final; são
identificadores distintos. Esta atualização não altera essas versões nem publica
uma Release.

A [SDD](especificacao_sdd.md) preserva os requisitos RF/RNF, as regras RN e os
contratos completos; os [critérios de aceitação](criterios_aceitacao.md) ligam esses
requisitos à suíte. Este As-Built registra sua realização e seus limites.

## 2. Arquitetura e fluxo implementados

Há uma aplicação FastAPI com rotas e acesso ao banco síncronos. O fluxo é:

**Cliente HTTP → FastAPI/Pydantic → função da rota → CRUD → sessão SQLAlchemy
→ SQLite → resposta HTTP.**

O [diagrama final](arquitetura.md#diagrama-final) e seu
[fonte Mermaid](diagramas/arquitetura-final.mmd) representam os componentes,
as respostas e a inicialização. A validação acontece antes da execução da função
da rota. Uma entrada inválida resulta em `422` sem alteração dos registros.

- `app/main.py` cria o FastAPI, registra o router e chama `init_db()` no `lifespan`.
- `app/database.py` configura URL, engine, sessões e criação das tabelas. `get_db()`
  fornece uma sessão por requisição e a fecha em `finally`.
- `app/schemas.py` valida/normaliza entradas e serializa saídas.
- `app/routes.py` define as quatro operações, valida IDs e converte ausência em `404`.
- `app/crud.py` consulta e altera registros; escritas fazem `commit`, com `rollback`
  se o commit falhar. Cadastro e atualização fazem `refresh` antes do retorno.
- `app/models.py` declara a única tabela de domínio, `tarefas`.
- `scripts/criar_banco.py` permite inicializar as tabelas sem subir o servidor.

GET apenas consulta, sem `commit`. PATCH e DELETE procuram o registro antes de
alterá-lo. A validação do corpo ocorre antes dessa busca: PATCH inválido para ID
válido inexistente retorna `422`; com corpo válido, retorna `404`.

## 3. Modelo e schemas

O modelo ORM `Tarefa` tem:

- `id`: `Integer`, chave primária gerada pelo SQLite. As rotas aceitam inteiros
  positivos até `9223372036854775807`. Não se garante sequência sem lacunas ou
  primeiro ID igual a 1 em qualquer banco.
- `titulo`: `String(120)`, não nulo. A aplicação exige string com 1 a 120 caracteres
  Unicode após `strip()`. Preserva espaços internos, acentos e caixa; títulos
  repetidos são permitidos. O tipo `String(120)` no SQLite não impõe esse limite.
- `concluida`: `Boolean`, não nulo, com padrão Python `False` e padrão de banco
  `"0"`. Uma tarefa criada pela API sempre nasce pendente.

Schemas Pydantic implementados:

- `TarefaCreate`: aceita somente `titulo`, obrigatório, normalizado e válido.
- `TarefaAtualizar`: aceita `titulo`, `concluida` ou ambos; exige pelo menos um.
  Um campo omitido preserva o valor atual. `null` explícito é rejeitado.
  `concluida` aceita exclusivamente o booleano JSON `true`, sem coerção de `1`
  ou `"true"`; `false` também é inválido. Editar o título não reabre a tarefa.
- `TarefaRead`: devolve `id`, `titulo` e `concluida` a partir do objeto ORM.
- `TarefaNaoEncontrada`: descreve `detail`, com padrão `"Tarefa não encontrada."`.
  As rotas reutilizam esse padrão como mensagem do erro real.

Os quatro schemas usam `extra="forbid"`. No PATCH, `model_fields_set` diferencia
omissão de `null`; `model_dump(exclude_unset=True)` entrega ao CRUD apenas os
campos enviados. Todos os campos são validados antes de persistir a alteração.

## 4. Contratos HTTP entregues

Endereço local padrão: `http://127.0.0.1:8000`. POST e PATCH recebem JSON com
`Content-Type: application/json`. As rotas canônicas não têm barra final.
Os IDs abaixo são ilustrativos; usar o ID retornado pelo cadastro.

### POST /tarefas

Entrada:

```json
{"titulo": "  Revisar documentação  "}
```

Resposta `201 Created`, após persistir:

```json
{"id": 1, "titulo": "Revisar documentação", "concluida": false}
```

Campo ausente, título inválido, campos extras, corpo ausente ou JSON malformado
retornam `422`, sem criar uma tarefa. O consumidor não pode informar `id` ou
`concluida` no cadastro.

### GET /tarefas

Retorna `200 OK` com todas as tarefas, pendentes e concluídas, por ID crescente.
Sem registros, retorna `[]`. Não há filtros ou paginação definidos.

```json
[{"id": 1, "titulo": "Revisar documentação", "concluida": false}]
```

### PATCH /tarefas/{id}

Aceita qualquer um destes corpos:

```json
{"titulo": "Revisar documentação final"}
```

```json
{"concluida": true}
```

```json
{"titulo": "Revisar documentação final", "concluida": true}
```

Retorna `200 OK` com a tarefa atualizada. Preserva o ID e os campos omitidos;
repetir a mesma atualização válida mantém o estado. Não cria outra tarefa.
Corpo vazio `{}`, campos extras, `null` ou `concluida=false` retornam `422`.
Se um campo for inválido, nenhum é alterado. ID válido inexistente com corpo
válido retorna `404`; entrada inválida retorna `422`.

### DELETE /tarefas/{id}

Retorna `204 No Content`, sem corpo, após excluir fisicamente a tarefa.
Excluir novamente o mesmo ID ainda ausente retorna `404`.
ID inválido retorna `422`.

### Erros

PATCH e DELETE retornam este corpo para ID válido inexistente e entrada válida:

```json
{"detail": "Tarefa não encontrada."}
```

O `422` segue a estrutura do FastAPI: `detail` é uma lista de erros com `loc`,
`msg` e `type`. Mensagens e campos adicionais podem variar com as dependências.
Não se exige uma frase específica em inglês nem ordem fixa de múltiplos erros.

## 5. Persistência e configuração

A URL padrão é `sqlite:///./tarefas.db`, relativa ao diretório de execução.
`TAREFAS_DATABASE_URL` pode substituí-la e precisa ser definida antes de importar
ou iniciar a aplicação. O diretório de destino precisa existir.

`init_db()` usa `Base.metadata.create_all()` para criar tabelas ausentes; não
executa migrações de tabelas existentes. Os registros persistem entre processos
que reutilizam o mesmo arquivo. No Docker, a URL é
`sqlite:////data/tarefas.db`; montar um volume em `/data` preserva o arquivo ao
recriar o container.

Os testes configuram banco temporário antes de importar a aplicação e substituem
`get_db()` por uma sessão isolada. Restauram overrides, fecham engines e removem
arquivos. Há testes de proteção do banco manual e de persistência entre processos.

## 6. Ambiente, execução e CI

As versões declaradas são FastAPI 0.141.1, Uvicorn 0.52.4, Pydantic 2.13.5,
SQLAlchemy 2.0.52, pytest 9.1.1 e HTTPX 0.28.1. `pytest-cov` está no extra `test`,
sem versão fixada. O projeto requer Python `>=3.12`; o Dockerfile e o workflow
selecionam 3.12.10. A conferência local usou 3.12.6.

Com ambiente virtual ativo e a partir da raiz:

```text
python -m pip install -e ".[test]"
python -m pip check
python -m uvicorn app.main:app --reload
```

Swagger: `/docs`; ReDoc: `/redoc`; esquema gerado: `/openapi.json`.
Em outro terminal com o mesmo ambiente, executar testes e cobertura:

```text
python -m pytest tests -v --cov=app --cov-report=term-missing
```

Os comandos completos de Docker, volume e relatórios estão no [README](../README.md).
Não há Compose: o projeto tem um único container e SQLite em arquivo.

O workflow `Testes e Docker` roda em PRs para `develop`/`main` e pushes nessas
branches. Instala dependências, executa `pip check`, roda testes com cobertura,
constrói a imagem e roda testes com cobertura no container. Publica `pytest.xml`,
`docker.xml`, `coverage.xml` e `coverage-docker.xml` em `resultados-testes`.
Esse fluxo é de integração contínua; não há deploy automático configurado.

## 7. Evidências e limites da verificação

Em 27/10/2026, na base acima, a execução local terminou com **81 testes aprovados,
um aviso de descontinuação e zero falhas**. A cobertura de linhas de `app/` foi
**91%** no terminal: 135 das 148 instruções contabilizadas. Não é cobertura de
branches; 100% dos testes aprovados não significa 100% de cobertura.

A [CI da base 668faae](https://github.com/gabrielavieirab/tarefas-api/actions/runs/40586231416)
concluiu com sucesso testes no runner, build e testes Docker, conforme os passos
do job consultados. Docker não está disponível neste ambiente local. Não se
atribui ao CI o percentual medido localmente nem se afirma teste operacional de
recriação do container com volume, que não faz parte desse workflow.

O [registro de evidências](evidencias_testes.md#entrega-final--27102026) identifica
comandos, versões e arquivos dos resultados. A comparação do OpenAPI gerado com
o contrato estático foi uma verificação adicional de documentação, fora da suíte
de 81 casos; não há teste de OpenAPI/Swagger nessa suíte.

## 8. Do planejamento à implementação

- **Escopo funcional:** o contrato 1.1.0 foi mantido. Edição de título já estava
  prevista em RF-08/RN-12; não é uma funcionalidade nova desta consolidação.
- **Documentação automática:** o [PR #26](https://github.com/gabrielavieirab/tarefas-api/pull/26)
  acrescentou as respostas `404` ao OpenAPI de PATCH/DELETE e um caso explícito
  de PATCH `{}`, elevando a suíte de 80 para 81. A auditoria do
  [PR #29](https://github.com/gabrielavieirab/tarefas-api/pull/29) removeu um import
  sem uso e centralizou a mensagem `404` no schema.
- **Ambiente:** o commit
  [`5c252e7`](https://github.com/gabrielavieirab/tarefas-api/commit/5c252e7201ac872bee99c16ab9d05a8407c33d7a)
  integrou a cobertura no runner e no Docker. A proposta de lock transitivo não
  foi adotada; `pytest-cov` também está sem pin e a imagem não tem digest.
- **Consolidação:** o PR #30 integrou a base documental. Esta revisão
  completa o As-Built, vincula os documentos existentes e registra evidências;
  não altera código, testes, dependências ou infraestrutura.

## 9. Limitações e fechamento

O OpenAPI gerado declara os `404`, mas ainda não expressa integralmente o limite
e a normalização do título, a proibição de `null`, a conclusão exclusivamente
com `true` e a exigência de PATCH não vazio. O contrato estático detalha essas
regras. Os dois documentos não são idênticos nem devem ser apresentados assim.

A cobertura local deixa sem execução medida os caminhos de `rollback` de commits
com falha e o corpo de `get_db()` nesta execução com overrides. Testes que usam
subprocessos não têm instrumentação adicional de cobertura configurada.
Não há requisito de alta concorrência/SLA, autenticação ou migrações; mudanças
nesse sentido exigem nova especificação. As decisões e consequências estão nos
[ADRs revisados](decisoes_tecnicas.md).

A [validação técnica final](validacao-tecnica-final.md) reúne as verificações
realizadas e as pendências de fechamento. A revisão do PDF depende da versão
consolidada.
