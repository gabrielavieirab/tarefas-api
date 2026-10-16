# Evidências de testes e CI

## Versão e ambiente

Validação local anterior ao versionamento em 07/09/2026, na branch `feature/testes-ci`.
Base: `6f137318340b29789a7e6291dc3a368c3b19668d`, igual a `origin/develop`
após o fetch. O resultado inclui as alterações locais ainda sem commit desta
contribuição; não representa uma execução da base sem alterações.

Ambiente da validação histórica: Windows, Python 3.12.10, pytest 9.1.1.
Dependências diretas registradas naquela validação: FastAPI 0.141.1, Uvicorn 0.52.4,
Pydantic 2.13.5, SQLAlchemy 2.0.52 e HTTPX 0.28.1.

Comandos executados na validação histórica com o Python 3.12 do ambiente virtual:

```text
python -m pip install -e ".[test]"
python -m pip check
python -m pytest -v --junitxml=../../outputs/pytest.xml
```

O destino do XML acima é uma pasta de evidências fora do repositório naquela
cópia de trabalho. Para reproduzir apenas a suíte, use `python -m pytest -v`.

Resultado da validação histórica:

```text
No broken requirements found.
collected 80 items
80 passed, 2 warnings in 18.79s
```

Foram 80 aprovados, zero falhas, zero erros e zero testes ignorados.
Os dois avisos registrados naquela execução estavam relacionados às dependências:
descontinuação do uso de HTTPX pelo TestClient do Starlette e do alias
`anyio.abc.BlockingPortal`. Não foram suprimidos.

Na validação histórica, nenhuma falha funcional da API foi encontrada e `app/`
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
| CA-26 | Testes locais, Docker e CI remoto executados com sucesso | Suíte local, testes no container e execução #16 do GitHub Actions |
| CA-27 a CA-31 | Cobertos e aprovados | Edição: `test_ca27_*` a `test_ca31_*` |

Os testes de modelo existentes foram preservados. A suíte passou de 64 para
80 casos durante o desenvolvimento, acrescentando valores de borda e asserções
onde faltavam.

O CA-23 inicia dois processos independentes da aplicação com o mesmo SQLite
temporário. Após o reinício, confirma título editado, tarefa concluída e exclusão.

O CA-24 executa casos de cadastro e banco vazio em outro processo, com e sem URL
configurada, bloqueia acessos ao banco manual e verifica restauração do ambiente,
dos overrides e remoção dos bancos temporários. Nenhum `.db` ficou no projeto.

## Docker

Configuração: `python:3.12.10-slim`, instalação das dependências de teste,
Uvicorn na porta 8000 e banco em `/data/tarefas.db`.

A construção da imagem Docker foi validada com sucesso:

```text
docker build -t tarefas-api .
```

A API foi iniciada na porta 8000 e validada pelo endpoint `/docs`.

Os testes automatizados também foram executados dentro do container:

```text
docker exec tarefas-api-container python -m pytest -v
80 passed, 1 warning
```

### Persistência do SQLite

Foi criado o volume Docker `tarefas-dados`, montado em `/data`.

A persistência foi validada criando tarefas pela API, parando e removendo
o container e recriando-o com o mesmo volume. Após a recriação, as tarefas
continuaram disponíveis pela API, confirmando a persistência dos dados.

Comando utilizado para iniciar o container com o volume:

```text
docker run -d --name tarefas-api-container -p 8000:8000 -v tarefas-dados:/data tarefas-api
```

A validação local anterior havia sido bloqueada por um erro do Docker Desktop
relacionado à disponibilidade da virtualização. Posteriormente, o Docker passou
a funcionar, permitindo construir a imagem, executar os testes no container
e verificar a persistência usando o volume.

## GitHub Actions

O arquivo `.github/workflows/tests.yml` foi validado anteriormente com
[actionlint 1.7.12](https://github.com/rhysd/actionlint/releases/tag/v1.7.12):

```text
actionlint .github/workflows/tests.yml
exit code: 0
```

Foi uma verificação estática, sem erros. A ferramenta foi usada fora do projeto
e não foi adicionada às suas dependências.

O workflow roda em pull requests direcionados às branches `develop` e `main`
e em pushes nessas branches. Utiliza Python 3.12.10, verifica o ambiente,
executa os testes no runner, constrói a imagem Docker, executa os testes
dentro do container e publica os relatórios XML como artefato.

### Execução remota

A execução remota foi realizada no GitHub Actions e terminou com sucesso.

- Branch: `main`
- Commit relacionado à correção dos relatórios: `8ecaf5f`
- Workflow: `Testes`
- Execução: #16
- Resultado: sucesso

Link do histórico de execuções:
https://github.com/gabrielavieirab/tarefas-api/actions

Para a evidência final, deve ser utilizado o link direto da execução #16,
copiado da barra de endereços do navegador.

### Relatórios XML

O workflow está configurado para gerar dois relatórios:

- `test-results/pytest.xml`: resultados dos testes executados no runner.
- `test-results/docker.xml`: resultados dos testes executados no container.

O passo `Guardar resultados` utiliza `actions/upload-artifact@v4`
para publicar o artefato `resultados-testes`.

A configuração de publicação está presente no workflow. A conferência final
do conteúdo do artefato deve confirmar que os dois arquivos XML estão
disponíveis para download na execução #16.

## Revisão e limites

- `git diff --check`: código 0, sem erros de whitespace na validação registrada.
- `git diff`: revisado anteriormente; alterações restritas a ambiente, testes,
  CI e documentação naquela contribuição.
- `git diff --exit-code -- app/`: código 0 na validação histórica, com a aplicação preservada.
- A situação do Git registrada anteriormente indicava arquivos desta contribuição
  ainda sem commit. Posteriormente, a correção do workflow foi registrada no commit
  `8ecaf5f`.
- Sem constraints/lock naquela etapa, conforme orientação. As dependências diretas
  foram fixadas no `pyproject.toml`; as transitivas podem variar. A fixação completa
  prevista no ADR-004 continua pendente de decisão, sem introduzir outro arquivo.
- Os testes locais e os testes dentro do container passaram, a imagem Docker foi
  construída e a execução remota do GitHub Actions terminou com sucesso.
- A confirmação final dos artefatos depende de verificar se o download de
  `resultados-testes` contém `pytest.xml` e `docker.xml`.
- A revisão do README deve confirmar que os comandos de instalação, testes e
  execução do container podem ser reproduzidos por outro integrante da equipe.