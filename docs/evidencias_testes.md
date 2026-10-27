# Evidências de testes e CI

## Entrega Final — 27/10/2026

Base: `develop` em `668faae7bdc54024c1b7c75ca483aa9adfe21d8d`.
Branch documental: `codex/documentacao-entrega3`. A aplicação, os testes,
as dependências e a infraestrutura permanecem iguais à base conferida.

### Execução local de Vitor

Ambiente Windows, Python **3.12.6**, pytest **9.1.1**, pytest-cov **7.1.0**,
coverage.py **7.17.0**. Instalação pelo extra `test` já declarado no projeto.
O Python local difere do **3.12.10** selecionado no Docker e no CI.

Comandos executados na raiz, usando `.venv/Scripts/python.exe`:

```text
python -m pip install -e ".[test]"
python -m pip check
python -m pytest tests -v --cov=app --cov-report=term-missing --cov-report=xml:test-results/entrega3-vitor/coverage.xml --junitxml=test-results/entrega3-vitor/pytest.xml
```

Resultado:

```text
No broken requirements found.
collected 81 items
TOTAL 148 statements, 13 missed, 91% covered
81 passed, 1 warning in 11.41s
```

São zero falhas, erros ou casos ignorados. O aviso é a descontinuação do uso de
HTTPX pelo TestClient do Starlette. Não foi ocultado. O relatório local contém:

- `test-results/entrega3-vitor/pytest.log`: saída completa da execução.
- `test-results/entrega3-vitor/pytest.xml`: resultado JUnit dos 81 casos.
- `test-results/entrega3-vitor/coverage.xml`: cobertura de linhas de `app/`.
- `test-results/entrega3-vitor/conferencia-documental.txt`: conferência adicional
  de contratos, exemplos e documentação.

Esses arquivos são locais e ignorados pelo Git. O resultado resumido permanece
versionado neste documento; os relatórios da CI são publicados como artefatos.

Cobertura local: **135/148 instruções, 91% arredondados no terminal**. Não foi
habilitada medição de branches nem instrumentação adicional de subprocessos.
Não há cobertura medida de `app/crud.py` nas linhas 21–23, 50–52 e 65–67
(rollback por falha de commit), nem de `app/database.py` nas linhas 63–67
(`get_db`, substituído por override nos testes HTTP desta execução).
Isso limita a interpretação da cobertura; não demonstra defeito nesses caminhos.

### Conferência adicional da documentação

Foi conferido o conjunto de quatro operações e seus códigos HTTP no OpenAPI
gerado contra `docs/openapi.json`, além dos exemplos de requisição do As-Built
contra o TestClient com SQLite temporário. A normalização do título, a conclusão
sem reabertura, os erros e o DELETE sem corpo também foram conferidos.
É uma verificação documental adicional; não foi acrescentada à contagem dos 81
testes e não representa teste automatizado de Swagger existente na suíte.

PATCH/DELETE já declaram `404` no OpenAPI gerado. Os schemas gerados ainda não
expressam todos os validadores personalizados; não se afirma igualdade integral
com o contrato estático.

### CI e Docker da base integrada

Execução pública consultada:
[GitHub Actions 40586231416](https://github.com/gabrielavieirab/tarefas-api/actions/runs/40586231416),
da `develop`, commit `668faae7bdc54024c1b7c75ca483aa9adfe21d8d`.
Estado `completed`, conclusão `success`. O
[job 122478212824](https://github.com/gabrielavieirab/tarefas-api/actions/runs/40586231416/job/122478212824)
registrou sucesso nos passos de instalação, `pip check`, testes no Python,
build da imagem, testes Docker e publicação dos resultados.

O workflow gera `pytest.xml`, `docker.xml`, `coverage.xml` e
`coverage-docker.xml`, no artefato `resultados-testes`. A consulta aos passos
confirma a execução da base; não foi usada para inferir um percentual remoto.
Os 91% acima são da execução local. A CI de um futuro PR documental deve ser
conferida separadamente, no respectivo commit.

Docker não está disponível neste ambiente local. Não houve build local nem
validação operacional da recriação de container com volume. Esse cenário não é
executado pelo workflow atual e segue para conferência de Caike/equipe.

Os registros históricos abaixo preservam as situações e resultados de cada data.

## Atualização da entrega 2 - 15/10/2026

### Base e execução local

Base obtida por pull de `main`:
[`8ecaf5f890ecfa4c2c4bbcefa378c03139b73e0d`](https://github.com/gabrielavieirab/tarefas-api/commit/8ecaf5f890ecfa4c2c4bbcefa378c03139b73e0d).
Branch de documentação: `codex/documentacao-entrega2`. A aplicação e os testes
não foram alterados nesta atualização.

Ambiente: Windows, Python **3.12.6**, pytest 9.1.1. Instalação em `.venv`,
com as dependências diretas fixadas no `pyproject.toml`. Essa versão de patch
local difere do Python **3.12.10** usado no CI e no Docker; os resultados
dos ambientes são registrados separadamente.

Comandos, a partir da raiz e usando o Python do ambiente virtual:

```text
python -m pip install -e ".[test]"
python -m pip check
python -m pytest tests -v --junitxml=test-results/pytest.xml
```

Resultado:

```text
No broken requirements found.
collected 80 items
80 passed, 1 warning in 9.99s
```

São 80 aprovações, zero falhas, zero erros e zero testes ignorados.
O aviso é `StarletteDeprecationWarning` sobre o uso de HTTPX pelo TestClient.
Ele foi mantido visível. Entre as dependências transitivas resolvidas estão
Starlette 1.8.0 e AnyIO 4.15.1; não há lock transitivo.
O XML fica em `test-results/pytest.xml`, diretório ignorado pelo Git.
O destino explícito `tests` evita coletar cópias antigas em pastas temporárias.

### CI e Docker confirmados na base integrada

Execução pública:
[GitHub Actions 38781864191](https://github.com/gabrielavieirab/tarefas-api/actions/runs/38781864191).
Branch: `main`. Commit: `8ecaf5f890ecfa4c2c4bbcefa378c03139b73e0d`.
Início: **15/10/2026, 14h59, horário de Brasília** (17h59 UTC).
Estado consultado: `completed`, conclusão `success`.

O [job de testes](https://github.com/gabrielavieirab/tarefas-api/actions/runs/38781864191/job/116583854401)
registrou sucesso na instalação, na conferência de ambiente, nos testes do
runner, no build Docker, nos testes no container e na publicação de resultados.
O artefato `resultados-testes` estava disponível e não expirado na consulta.
O workflow usa Python 3.12.10, gera `pytest.xml` e `docker.xml` e monta o
diretório dos relatórios do runner em `/resultados` no container.

Essa evidência atualiza a pendência de execução remota descrita no registro
histórico abaixo. O CA-26 tem execução local e de CI com container comprovadas.
O Docker não estava instalado/disponível no ambiente local desta atualização;
não se afirma um build local. A execução pública não testa a recriação de
containers com o volume de dados, cuja validação operacional cabe à equipe.
A CI citada corresponde à base integrada, não a um PR desta atualização documental.

### Conferência antes do PR documental

Após a integração do PR #18 de Gabriela, a contribuição de Vitor foi aplicada
sobre `develop` em `1b6294a`. A comparação com essa base confirma alterações
somente em documentação, preservando aplicação, testes, dependências, Dockerfile
e workflow. A correção de CI do commit `8ecaf5f` permanece uma referência da
`main`, sem ser introduzida por este PR documental.

O comando `python -m pytest tests -v --junitxml=test-results/pytest-pre-pr.xml`
foi executado antes da publicação: **80 aprovados, um aviso, zero falhas,
zero erros e zero ignorados**, em 9,48 segundos. `python -m pip check`
também passou. Foram conferidos os links locais dos documentos da contribuição,
os blocos Markdown, a preservação dos esquemas do contrato estático e o diff.
O XML dessa conferência fica em `test-results/pytest-pre-pr.xml`, ignorado pelo Git.

A contribuição foi publicada no
[PR #25](https://github.com/gabrielavieirab/tarefas-api/pull/25), para `develop`,
vinculado à [Issue #22](https://github.com/gabrielavieirab/tarefas-api/issues/22).
Os checks desse PR apresentam a execução de CI específica da contribuição.
Sua revisão humana e integração são acompanhadas separadamente dos testes.

## Registro histórico - validação de 07/09/2026

As seções seguintes preservam os resultados e pendências registrados na época.
Para a situação de 15/10/2026, considere a atualização acima.

### Versão e ambiente

Validação local anterior ao versionamento em 07/09/2026, na branch `feature/testes-ci`.
Base: `6f137318340b29789a7e6291dc3a368c3b19668d`, igual a `origin/develop`
após o fetch. O resultado inclui as alterações locais ainda sem commit desta
contribuição; não representa uma execução da base sem alterações.

Ambiente: Windows, Python 3.12.10, pytest 9.1.1.
Dependências diretas: FastAPI 0.141.1, Uvicorn 0.52.4, Pydantic 2.13.5,
SQLAlchemy 2.0.52 e HTTPX 0.28.1.

Comandos executados com o Python 3.12 do ambiente virtual:

```text
python -m pip install -e ".[test]"
python -m pip check
python -m pytest -v --junitxml=../../outputs/pytest.xml
```

O destino do XML acima é uma pasta de evidências fora do repositório nesta
cópia de trabalho. Para reproduzir apenas a suíte, use `python -m pytest -v`.

Resultado:

```text
No broken requirements found.
collected 80 items
80 passed, 2 warnings in 18.79s
```

Foram 80 aprovados, zero falhas, zero erros e zero testes ignorados.
Os dois avisos vêm das dependências: descontinuação do uso de HTTPX pelo
TestClient do Starlette e do alias `anyio.abc.BlockingPortal`.
Não foram suprimidos. Nenhuma falha funcional da API foi encontrada e `app/`
não foi alterado.

### Critérios de aceitação em 07/09/2026

| Critérios | Resultado local | Testes relacionados |
|---|---|---|
| CA-01 a CA-08 | Cobertos e aprovados | Cadastro: `test_ca01_*` a `test_ca08_*` |
| CA-09 a CA-11 | Cobertos e aprovados | Listagem: `test_ca09_*` a `test_ca11_*` |
| CA-12 a CA-17 | Cobertos e aprovados | Conclusão e validação: `test_ca12_*` a `test_ca17_*` |
| CA-18 a CA-22 | Cobertos e aprovados | Exclusão e IDs: `test_ca18_*` a `test_ca22_*` |
| CA-23 | Coberto e aprovado em Python 3.12 | `test_rf07_persistencia_entre_reinicializacoes` |
| CA-24 | Coberto e aprovado | `test_ca24_banco_manual_e_limpeza` e fixtures |
| CA-25 | Coberto e aprovado | `test_ca25_formato_das_respostas` |
| CA-26 | Parcial: execução local aprovada | Container e execução remota pendentes |
| CA-27 a CA-31 | Cobertos e aprovados | Edição: `test_ca27_*` a `test_ca31_*` |

Os testes de modelo existentes foram preservados. A suíte passou de 64 para
80 casos, acrescentando valores de borda e asserções onde faltavam.

O CA-23 inicia dois processos independentes da aplicação com o mesmo SQLite
temporário. Após o reinício, confirma título editado, tarefa concluída e exclusão.
O CA-24 executa casos de cadastro e banco vazio em outro processo, com e sem URL
configurada, bloqueia acessos ao banco manual e verifica restauração do ambiente,
dos overrides e remoção dos bancos temporários. Nenhum `.db` ficou no projeto.

### Docker em 07/09/2026

Configuração: `python:3.12.10-slim`, instalação de `.[test]`, Uvicorn na
porta 8000 e banco em `/data/tarefas.db`. O README documenta um volume persistente.

Foi tentado:

```text
docker build -t tarefas-api:test .
```

O comando terminou com código 1 antes do build. O Docker Desktop local respondeu:

```text
500 Internal Server Error
http://%2F%2F.%2Fpipe%2FdockerDesktopLinuxEngine/_ping
```

O Dockerfile foi revisado, mas não houve imagem construída nem testes executados
no container. Na revisão, Caike confirmou que o Docker Desktop não inicia porque
a virtualização não está habilitada/disponível no computador. A validação do
container será feita no GitHub Actions, sem alterar o Dockerfile para contornar
essa limitação local. Não foi alterada a configuração do sistema para corrigir o Docker.

### GitHub Actions em 07/09/2026

O arquivo `.github/workflows/tests.yml` foi validado com
[actionlint 1.7.12](https://github.com/rhysd/actionlint/releases/tag/v1.7.12):

```text
actionlint .github/workflows/tests.yml
exit code: 0
```

Foi uma verificação estática, sem erros. A ferramenta foi usada fora do projeto
e não foi adicionada às suas dependências.

O workflow roda em PRs para develop/main e pushes nessas branches, usa Python
3.12.10, executa pytest localmente no runner e no container e guarda relatórios XML.
Na etapa de validação local não houve execução remota. O resultado remoto deve
ser conferido na aba Checks do Pull Request e no histórico do GitHub Actions.

### Revisão e limites em 07/09/2026

- `git diff --check`: código 0, sem erros de whitespace.
- `git diff`: revisado; alterações restritas a ambiente, testes, CI e documentação.
- `git diff --exit-code -- app/`: código 0, aplicação preservada.
- `git status --short`: apenas os arquivos desta contribuição, ainda sem commit.
- Sem constraints/lock nesta etapa, conforme orientação. As dependências diretas
  foram fixadas no pyproject; as transitivas podem variar. A fixação completa
  prevista no ADR-004 continua pendente de decisão, sem introduzir outro arquivo.
- CA-26 permanece parcial até validação real de Docker e CI.
