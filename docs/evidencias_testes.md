# Evidências de testes e CI

## Versão e ambiente

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

## Critérios de aceitação

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

## Docker

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

## GitHub Actions

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

## Revisão e limites

- `git diff --check`: código 0, sem erros de whitespace.
- `git diff`: revisado; alterações restritas a ambiente, testes, CI e documentação.
- `git diff --exit-code -- app/`: código 0, aplicação preservada.
- `git status --short`: apenas os arquivos desta contribuição, ainda sem commit.
- Sem constraints/lock nesta etapa, conforme orientação. As dependências diretas
  foram fixadas no pyproject; as transitivas podem variar. A fixação completa
  prevista no ADR-004 continua pendente de decisão, sem introduzir outro arquivo.
- CA-26 permanece parcial até validação real de Docker e CI.
