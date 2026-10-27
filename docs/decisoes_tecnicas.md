# Decisões técnicas e arquitetura

Decisões registradas inicialmente em 05/09/2026 e revisadas em 27/10/2026.
Estado: **escolhas conferidas na base `668faae` da develop**, consolidada na
[especificação As-Built](especificacao-as-built.md). As decisões são mantidas;
esta revisão registra sua implementação e seus limites. A aprovação humana
desta contribuição será registrada no respectivo PR.
ADR significa registro de uma decisão arquitetural: contexto, escolha, justificativa
e consequências. As escolhas priorizam facilidade de aprendizado, execução e
verificação no escopo acadêmico, preservando as tecnologias do `AGENTS.md`.
A [arquitetura detalhada](arquitetura.md) descreve o fluxo implementado.

## ADR-001 - Python e FastAPI

**Contexto.** São quatro operações HTTP, um modelo simples e necessidade de validar
entradas, documentar contratos e executar testes.

**Decisão.** Python 3.12, FastAPI e Uvicorn. Pydantic 2 para os esquemas de entrada
e saída. Usar rotas síncronas (`def`) junto do acesso síncrono ao banco.

**Justificativa.** O FastAPI integra validação e documentação OpenAPI e oferece um
cliente para testes. Isso reduz a configuração para demonstrar os contratos.
Python também já aparece nas Issues #4 e #8 e nas instruções da equipe.

**Alternativas consideradas.** Flask é uma opção pequena, mas exigiria selecionar
e integrar mais ferramentas para validação e documentação. Express seria adequado
a uma equipe já familiarizada com JavaScript, porém mudaria o plano iniciado.
Não há evidência de maior familiaridade do grupo com outra linguagem que justifique
essa troca neste momento.

**Consequências.** O grupo precisa conhecer modelos Pydantic e sessões do banco.
Python 3.12 é a linha de referência do projeto. O container e o CI fixam
3.12.10. A execução documental de 27/10/2026 usou 3.12.6, diferença registrada
nas evidências. FastAPI 0.141.1, Pydantic 2.13.5 e Uvicorn 0.52.4 estão
fixados no `pyproject.toml` e são usados em `app/main.py` e `app/schemas.py`.

Fontes: [corpos de requisição](https://fastapi.tiangolo.com/tutorial/body/) e
[testes do FastAPI](https://fastapi.tiangolo.com/tutorial/testing/).

## ADR-002 - SQLite e SQLAlchemy

**Contexto.** A API usa uma única tabela, poucos dados na demonstração e precisa
preservar registros entre execuções.

**Decisão.** SQLite em arquivo local, acessado pelo ORM síncrono do SQLAlchemy 2.
Usar uma tabela `tarefas`, sem relacionamentos, um engine por aplicação e uma
sessão por requisição. Usar consultas parametrizadas pelo ORM.

**Justificativa.** SQLite dispensa servidor de banco, credenciais e um segundo
container. O SQLAlchemy já foi registrado no `AGENTS.md` e permite concentrar
consultas e transações em um módulo pequeno.

**Alternativas consideradas.** O módulo `sqlite3` da biblioteca padrão reduziria
dependências, mas exigiria SQL e conversão de registros manuais. SQLModel é viável,
porém acrescentaria outra abstração sobre uma escolha já documentada. PostgreSQL
e MySQL exigiriam mais configuração sem resolver uma necessidade desta entrega.

**Consequências.** SQLAlchemy tem um custo de aprendizado pequeno, mas real; a
implementação deve se limitar a criar, selecionar, atualizar e excluir registros.
SQLite não é a escolha para múltiplos servidores gravando no mesmo arquivo.
Um processo da API é suficiente para a demonstração. O Docker aponta para
`/data/tarefas.db`; o comando documentado monta um volume nesse diretório.
Os testes usam arquivos temporários independentes. A persistência entre processos
foi testada; a conferência operacional do volume fica na validação de ambiente.

**Implementação.** SQLAlchemy 2.0.52, `criar_engine()`, `get_db()` e `init_db()`
em `app/database.py`; modelo em `app/models.py`; operações em `app/crud.py`.
Não foi adicionado serviço de banco, camada genérica de repositórios ou migração.

Fonte: [usos adequados do SQLite](https://www.sqlite.org/whentouse.html) e
[guia inicial do SQLAlchemy 2](https://docs.sqlalchemy.org/en/20/orm/quickstart.html).

## ADR-003 - Contratos pequenos e explícitos

**Contexto.** As rotas e campos já estão acordados; ainda faltava eliminar
ambiguidades que poderiam gerar implementações e testes incompatíveis.

**Decisão.** POST recebe apenas `titulo`; PATCH recebe `titulo`, `concluida: true`
ou ambos, exigindo pelo menos um campo e preservando os campos omitidos;
DELETE retorna `204` sem corpo. Usar `422` para validação e `404` para registro
inexistente com entrada válida. Listar por ID crescente. Normalizar extremidades
do título, com limite de 120 caracteres após normalização. Permitir títulos iguais.

**Justificativa.** Um limite curto é suficiente para nomear uma tarefa e fácil de
testar. PATCH explícito evita que um corpo vazio produza uma mudança de estado por
engano. Aceitar só `true` mantém o escopo de conclusão, sem introduzir reabertura.
Reutilizar o PATCH para editar o texto permite corrigir digitação ou mudar a
atividade sem excluir e cadastrar outra tarefa, sem acrescentar rotas ou tabelas.
Campos extras rejeitados tornam erros de integração visíveis.

**Consequências.** É preciso validar o tipo booleano estritamente: valores como
`1` ou `"true"` não podem ser convertidos silenciosamente. A implementação usa
um validador `mode="before"` com `v is not True`, rejeitando coerções antes de
validar o booleano. Para o título, `_validar_titulo()` normaliza antes de verificar
o tamanho e é reutilizado em POST/PATCH. `model_fields_set` distingue omissão de
`null` explícito e detecta PATCH vazio. A rota usa
`model_dump(exclude_unset=True)` para aplicar apenas os campos enviados,
depois de validar o corpo todo.
Essas regras são escolhas do projeto, não exigências adicionais do professor.

**Limite conhecido.** Os validadores personalizados garantem essas regras na
execução, mas o OpenAPI gerado pelo FastAPI não descreve todas elas. O contrato
estático permanece a referência detalhada e a suíte verifica o comportamento.
As respostas 404 de PATCH/DELETE já estão declaradas no esquema gerado, após
o PR #26. O PR #29 centralizou a mensagem do erro no valor padrão de
`TarefaNaoEncontrada.detail`, reutilizado nas rotas. Completar os demais
metadados dos validadores continua uma pendência documental; a conferência
OpenAPI é registrada separadamente da suíte de testes.

Fontes: [modo estrito do Pydantic](https://docs.pydantic.dev/latest/concepts/strict_mode/)
e [validadores](https://docs.pydantic.dev/latest/concepts/validators/).

## ADR-004 - Ambiente e validação

**Contexto.** O roteiro pede execução reproduzível, testes e evidências. As Issues
#6 e #8 já preveem Docker e GitHub Actions.

**Decisão.** `venv` e pip no desenvolvimento; `pyproject.toml` com grupo opcional
`test` para preservar `python -m pip install -e ".[test]"`, comando existente em
`AGENTS.md`. pytest, TestClient e HTTPX para testes. Um Dockerfile da API e um
workflow do GitHub Actions para executar a suíte em PRs destinados a `develop` e
`main` e após integrações nessas branches.

**Justificativa.** Reutiliza os comandos já registrados, permite testar as rotas
sem iniciar um servidor HTTP separado e atende às tarefas de ambiente e CI.

**Implementação e ajuste da decisão.** O
[PR #15](https://github.com/gabrielavieirab/tarefas-api/pull/15) integrou o
ambiente, os testes e o CI. Docker e CI fixam Python 3.12.10. Na Entrega Final,
o commit `5c252e7` acrescentou `pytest-cov` ao extra `test`, sem pin, e medição
de cobertura no runner e no container. O workflow atual instala o projeto,
executa `pip check`, testa no runner, constrói a imagem e testa no container.
Publica `pytest.xml`, `docker.xml`, `coverage.xml` e `coverage-docker.xml`
em `resultados-testes`. A
[CI de 27/10/2026](https://github.com/gabrielavieirab/tarefas-api/actions/runs/40586231416)
da base `668faae` concluiu esses passos com sucesso. Não há deploy automático.

**Consequências.** A proposta inicial previa constraints/lock também para
dependências transitivas. O estado integrado adotou apenas pins diretos, conforme
registrado nas [evidências](evidencias_testes.md). Essa diferença é explicitada
nesta consolidação: instalações não são idênticas por definição, pois `pytest-cov`,
as transitivas e a tag da imagem sem digest podem variar. Fixação completa é uma melhoria futura
a avaliar com Caike; esta atualização não adiciona dependências ou outro lock.

Para os testes, cada caso deve ter banco SQLite temporário limpo e descartável.
A sobrescrita da dependência de sessão também precisa ser desfeita. A inicialização
dos testes não deve criar ou acessar o banco de uso manual. Preferir arquivo
temporário à memória compartilhada, para simplificar a configuração entre conexões.
O projeto entregue não tem Docker Compose, serviço de banco separado ou deploy.
Um container e um volume são suficientes para o escopo local documentado.

Fontes: [teste de banco no FastAPI](https://fastapi.tiangolo.com/how-to/testing-database/),
[testes do FastAPI](https://fastapi.tiangolo.com/tutorial/testing/) e
[Python no GitHub Actions](https://docs.github.com/en/actions/tutorials/build-and-test-code/python).

## ADR-005 - Branches, PRs e evidências de integração

**Contexto.** A entrega exige rastrear contribuições e revisão entre pares,
além de apresentar código e testes funcionando.

**Decisão.** Trabalhar por Issue e branch própria, integrar por PR para
`develop`, executar a CI e obter revisão de outro integrante antes do merge.
A versão estável chega a `main` por PR de integração. Vitor prepara a
documentação técnica; Felipe revisa o conteúdo e Gabriela confere a aderência
à atividade. Uma ferramenta de IA não substitui essa aprovação humana.

**Justificativa.** O PR concentra o diff, a discussão e o resultado dos testes.
Relacionar cada mudança ao contrato e ao teste permite explicar por que ela
foi feita e avaliar seu impacto.

**Consequências.** CI aprovada não comprova revisão humana. O histórico confirma
as integrações pelos PRs #12, #14, #15, #16 e #17, mas as evidências de review
devem ser citadas separadamente. Há
[aprovação de Caike no PR #16](https://github.com/gabrielavieirab/tarefas-api/pull/16#pullrequestreview-5188617537).
Na consulta de 15/10/2026, os PRs #12 e #15 não possuem reviews formais
registrados. Não são marcados como aprovados por colegas nesta consolidação.

## Decomposição em componentes

Estrutura implementada e integrada pelos PRs de aplicação e testes:

```text
app/
  __init__.py
  main.py           # cria a aplicação, inicializa o banco e registra as rotas
  database.py       # URL, engine e dependência de sessão
  models.py         # modelo SQLAlchemy Tarefa e metadados da tabela
  schemas.py        # entrada, saída e TarefaNaoEncontrada (Pydantic)
  crud.py           # criar, listar, atualizar e excluir no banco
  routes.py         # quatro operações HTTP e tradução de ausência para 404
tests/
  conftest.py       # cliente, banco temporário e isolamento por teste
  test_tarefas.py   # cenários HTTP e persistência entre processos
  test_models.py    # integridade e persistência do modelo
  test_isolamento.py # proteção do banco manual e limpeza
scripts/
  criar_banco.py    # inicialização opcional sem servidor
```

**Fluxo interno:** cliente envia HTTP; a rota valida ID e corpo pelos esquemas;
o módulo de persistência realiza a operação com a sessão recebida; a rota devolve
o esquema de saída e o código HTTP. Não é necessária uma camada genérica de serviços
ou repositórios além desse módulo de operações.

**Interface dos componentes:**

- `TarefaCreate`: somente `titulo`, com validação estrita, normalização e limite.
- `TarefaAtualizar`: `titulo` e/ou `concluida`, com pelo menos um campo;
  título normalizado e válido, booleano estrito com valor `true` e sem `null`.
- `TarefaRead`: `id`, `titulo` e `concluida`; serialização de instância do ORM.
- `TarefaNaoEncontrada`: schema do 404 e fonte da mensagem usada pelas rotas.
- `criar_tarefa(sessao, titulo)`: recebe título já validado, persiste e retorna a tarefa.
- `listar_tarefas(sessao)`: retorna lista ordenada por ID, incluindo concluídas.
- `atualizar_tarefa(sessao, id, alteracoes)`: recebe um dicionário não vazio com
  somente os campos enviados e já validados; retorna a tarefa persistida ou
  `None` se não existir. Preserva campos omitidos e confirma a atualização inteira.
- `excluir_tarefa(sessao, id)`: retorna verdadeiro após excluir ou falso se ausente.
- `get_db()`: fornece uma sessão por requisição e sempre a fecha ao terminar.

O módulo CRUD confirma escritas antes de sinalizar sucesso; a sessão é revertida
quando uma transação falha. A camada de rotas transforma ausência em `404`, mantendo
os detalhes HTTP fora das operações de persistência. A configuração do banco deve
permitir URL de teste independente, inclusive na inicialização da aplicação.

## Feedback de custo-benefício

A escolha concentra a configuração em uma aplicação e um arquivo de banco. A
vantagem para esta entrega está na validação de dados, na documentação das rotas e
na facilidade de executar testes. O principal custo é aprender o básico de Pydantic,
SQLAlchemy, Docker e PRs; limitar cada ferramenta ao escopo definido mantém esse
custo controlado. A escolha não depende de contratar hospedagem ou banco externo.

Os 81 testes aprovados em 27/10/2026 e a CI com container sustentam a viabilidade
da solução no escopo atual. A cobertura local é 91% de linhas, não 100%.
A defesa técnica considera também os custos:

- FastAPI/Pydantic reduzem a configuração de validação e documentação, mas
  validadores personalizados precisam de testes e de metadados OpenAPI complementares.
- SQLite evita operar um servidor de banco, com a limitação de um arquivo local
  compartilhado e sem requisitos estabelecidos para múltiplos servidores.
- SQLAlchemy centraliza consultas e transações, ao custo de aprender engine,
  sessão e mapeamento ORM para uma única tabela.
- O PATCH parcial permite corrigir texto sem recriar a tarefa, exigindo distinguir
  omissão de `null` e preservar os demais campos. A reabertura permanece fora do escopo.
- Docker e CI verificam instalação e execução em outro ambiente; isso não
  substitui revisão humana nem comprova por si só a persistência operacional do volume.
- Pins das dependências principais tornam explícitas suas versões, mas `pytest-cov`
  sem pin e a ausência de lock transitivo limitam a reprodução exata.

Feedback novo, dificuldade de implementação ou mudança de requisito deve gerar
um registro em [Refinamentos](refinamentos.md) antes de alterar o contrato.
