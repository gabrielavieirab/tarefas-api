# Decisões técnicas e arquitetura

Registrei as decisões técnicas abaixo em 05/09/2026.
Estado dos ADRs: **propostos para revisão**.
ADR significa registro de uma decisão arquitetural: contexto, escolha, justificativa
e consequências. A escolha prioriza facilidade de aprendizado e execução para a
entrega inicial, preservando as tecnologias já indicadas no `AGENTS.md`.

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
Python 3.12 é a linha de referência do projeto, não uma alegação de ser a versão
mais recente. Caike deve usar a mesma linha localmente, no container e no CI.

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
Um processo da API é suficiente para a demonstração. Preservar o arquivo em volume
no Docker e usar um arquivo temporário independente nos testes.

Fonte: [usos adequados do SQLite](https://www.sqlite.org/whentouse.html) e
[guia inicial do SQLAlchemy 2](https://docs.sqlalchemy.org/en/20/orm/quickstart.html).

## ADR-003 - Contratos pequenos e explícitos

**Contexto.** As rotas e campos já estão acordados; ainda faltava eliminar
ambiguidades que poderiam gerar implementações e testes incompatíveis.

**Decisão.** POST recebe apenas `titulo`; PATCH exige `{"concluida": true}`;
DELETE retorna `204` sem corpo. Usar `422` para validação e `404` para registro
inexistente com entrada válida. Listar por ID crescente. Normalizar extremidades
do título, com limite de 120 caracteres após normalização. Permitir títulos iguais.

**Justificativa.** Um limite curto é suficiente para nomear uma tarefa e fácil de
testar. PATCH explícito evita que um corpo vazio produza uma mudança de estado por
engano. Aceitar só `true` mantém o escopo de conclusão, sem introduzir reabertura.
Campos extras rejeitados tornam erros de integração visíveis.

**Consequências.** É preciso validar o tipo booleano estritamente: valores como
`1` ou `"true"` não podem ser convertidos silenciosamente. Recomenda-se `StrictBool`
com validação de valor verdadeiro; uma checagem de igualdade simples com `True`
não é suficiente em Python. Para o título, normalizar antes de verificar o tamanho.
Essas regras são escolhas do projeto, não exigências adicionais do professor.

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

**Consequências.** Caike deve validar e fixar versões compatíveis dos pacotes,
inclusive dependências transitivas em arquivo de constraints/lock, e usar esse
arquivo no comando efetivo de instalação local, Docker e CI. A imagem deve ter uma
versão de patch ou digest registrado na configuração final. Esses arquivos e a
escolha dos pins são parte da Issue #6, após executar a aplicação de Felipe.

Para os testes, cada caso deve ter banco SQLite temporário limpo e descartável.
A sobrescrita da dependência de sessão também precisa ser desfeita. A inicialização
dos testes não deve criar ou acessar o banco de uso manual. Preferir arquivo
temporário à memória compartilhada, para simplificar a configuração entre conexões.
Não há necessidade inicial de Docker Compose, serviço de banco separado ou deploy.

Fontes: [teste de banco no FastAPI](https://fastapi.tiangolo.com/how-to/testing-database/),
[testes do FastAPI](https://fastapi.tiangolo.com/tutorial/testing/) e
[Python no GitHub Actions](https://docs.github.com/en/actions/tutorials/build-and-test-code/python).

## Decomposição em componentes

Estrutura proposta para Felipe e Caike implementarem. Os nomes abaixo são pontos
de acordo; os arquivos de aplicação ainda não fazem parte desta contribuição.

```text
app/
  __init__.py
  main.py           # cria a aplicação, inicializa o banco e registra as rotas
  database.py       # URL, engine e dependência de sessão
  models.py         # modelo SQLAlchemy Tarefa e metadados da tabela
  schemas.py        # TarefaCreate, TarefaConcluir e TarefaRead (Pydantic)
  crud.py           # criar, listar, concluir e excluir no banco
  routes.py         # quatro operações HTTP e tradução de ausência para 404
tests/
  conftest.py       # cliente, banco temporário e isolamento por teste
  test_tarefas.py   # cenários de aceitação
```

**Fluxo interno:** cliente envia HTTP; a rota valida ID e corpo pelos esquemas;
o módulo de persistência realiza a operação com a sessão recebida; a rota devolve
o esquema de saída e o código HTTP. Não é necessária uma camada genérica de serviços
ou repositórios além desse módulo de operações.

**Interface dos componentes:**

- `TarefaCreate`: somente `titulo`, com validação estrita, normalização e limite.
- `TarefaConcluir`: somente `concluida`, booleano estrito com valor `true`.
- `TarefaRead`: `id`, `titulo` e `concluida`; serialização de instância do ORM.
- `criar_tarefa(sessao, titulo)`: recebe título já validado, persiste e retorna a tarefa.
- `listar_tarefas(sessao)`: retorna lista ordenada por ID, incluindo concluídas.
- `concluir_tarefa(sessao, id)`: retorna a tarefa persistida ou `None` se não existir.
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

Se Felipe ou Caike identificarem uma dificuldade concreta na revisão, registrarei
a alternativa e o impacto antes da mudança. Não ampliar a API para justificar uma
tecnologia: os critérios de entrega e a facilidade de execução orientam a escolha.
