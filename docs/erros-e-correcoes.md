# Relatório de erros — Entrega 2 (Felipe)

Auditoria de `app/main.py`, `routes.py`, `schemas.py`, `crud.py`, `models.py` e
`database.py`, conforme a Seção 5.1 de "Divisão de Trabalho — Entrega 2".

## Escopo verificado

- Suíte de testes executada do zero (ambiente limpo, Python 3.12, dependências
  conforme `pyproject.toml`): **81 passed, 1 warning** (80 testes originais +
  1 teste novo adicionado nesta auditoria — ver tabela abaixo).
- Código de `app/` conferido linha a linha; nenhuma divergência encontrada em
  relação ao especificado em `docs/especificacao_sdd.md` além do item descrito
  abaixo.
- Comportamento confirmado manualmente (fora da suíte, via `TestClient`) para:
  POST, GET, PATCH (título, conclusão e ambos), DELETE, persistência entre
  reinicializações, títulos vazios/ausentes, campos extras, tipos inválidos,
  IDs fora do limite (`0`, negativo, não inteiro, acima de 2⁶³-1), PATCH vazio
  (`{}`) e preservação dos campos omitidos no PATCH.
- Schema OpenAPI gerado em tempo de execução (`app.openapi()`) comparado com o
  contrato `docs/openapi.json`. **O que foi validado, especificamente:** após
  a correção abaixo, os quatro endpoints coincidem exatamente nos **códigos de
  resposta HTTP** documentados (200/201/204, 404 e 422 em cada rota), que é o
  que a RNF-07 exige ("descrever o comportamento implementado"). **O que não
  coincide** (diferença real, confirmada por diff campo a campo, e que não é
  objeto desta correção): `operationId`, as descrições em prosa de cada
  resposta (o contrato tem texto específico, ex. "Tarefa criada e
  persistida."; o schema gerado traz o texto genérico do FastAPI, "Successful
  Response") e os `example`/`examples` de requisição e resposta, presentes no
  contrato mas não auto-gerados pelo FastAPI a partir do código atual. Nenhuma
  dessas diferenças afeta o comportamento da API nem os códigos de status.

## Tabela de erros e correções

| Problema | Identificação | Correção | Teste/PR |
|---|---|---|---|
| Documentação automática (`/docs`, `/openapi.json`) não listava o código `404` para `PATCH /tarefas/{id}` e `DELETE /tarefas/{id}`, apesar do comportamento em runtime estar correto (RNF-07 exige que a documentação automática descreva o comportamento implementado). Causa: `TarefaNaoEncontrada` (schema do erro 404) estava definido em `schemas.py` mas nunca referenciado nos decoradores de rota. | Comparação manual entre o schema OpenAPI gerado (`app.openapi()`) e o contrato `docs/openapi.json`: o contrato já previa `404` para essas duas rotas, mas o schema gerado só trazia `200`/`204` e `422`. | Adicionado `responses={404: {"model": TarefaNaoEncontrada, ...}}` aos decoradores `@router.patch("/tarefas/{id}", ...)` e `@router.delete("/tarefas/{id}", ...)` em `app/routes.py`, e incluído `TarefaNaoEncontrada` no import de `app.schemas`. | Nenhum teste de comportamento quebrou (81/81 continuam passando) — a mudança é só de documentação/contrato, não de lógica. Verificação feita regerando `app.openapi()` e comparando os **códigos de resposta HTTP** com `docs/openapi.json` (4 rotas, todas `OK` nos códigos). Descrições em prosa e `examples` do contrato não são auto-gerados pelo FastAPI e continuam diferentes — ver detalhe em "Escopo verificado", não fazem parte desta correção. PR: "Código e testes" (Responsável: Felipe, Revisor: Caike). |
| Lacuna de cobertura de teste: nenhum teste enviava `PATCH /tarefas/{id}` com corpo `{}` (JSON vazio, mas corpo presente) — só havia teste de PATCH *sem* corpo algum (`test_ca14_corpo_ausente_ou_malformado`), caso diferente. A Seção 5.1 pede explicitamente verificar "PATCH vazio". | Revisão da suíte (`grep` por `json={}` nos testes de PATCH) comparada com a lista de cenários exigidos no PDF. | Comportamento em si já estava correto (`{}` já retornava `422` por causa do validador `_ao_menos_um_campo`, que exige `model_fields_set` não vazio) — não foi necessária correção de código. Foi adicionado o teste `test_ca14_corpo_json_vazio_e_rejeitado` em `tests/test_tarefas.py`, cobrindo esse cenário explicitamente. | `test_ca14_corpo_json_vazio_e_rejeitado` (novo, passando). PR: "Código e testes" (Responsável: Felipe, Revisor: Caike). |

## Observação fora do escopo da Seção 5 (não corrigida aqui)

`pyproject.toml` está em `requires-python = ">=3.12"` com versões fixas de
dependências (provavelmente ajustado por outro integrante para a CI/Docker).
Isso diverge do ambiente local de Felipe, que está em Python 3.14.

**Validação efetivamente realizada** (ambiente de auditoria, Linux): a suíte
completa (81 testes) foi executada tanto em Python 3.12 quanto em Python
3.14.6, com as mesmas versões fixas de dependência do `pyproject.toml`
instaladas nos dois ambientes. Resultado: **81 passed nos dois**, schema
OpenAPI gerado (`app.openapi()`) **idêntico byte a byte** entre as duas
versões, schema SQL da tabela `tarefas` (criado via
`scripts/criar_banco.py`) **idêntico** nas duas, e os mesmos casos de borda
verificados manualmente (PATCH `{}`, PATCH com `concluida` não-booleano,
título com 120 caracteres Unicode) **com o mesmo resultado** nas duas
versões. Não foi encontrada nenhuma diferença de comportamento entre 3.12 e
3.14 para este código.

**O que essa validação não cobre:** foi feita em Linux, não no Windows real
de Felipe. O bug anteriormente observado (`PermissionError: WinError 32` no
encerramento dos testes) era específico do Windows, não da versão do Python,
e já foi corrigido por outro integrante no `tests/conftest.py` atual (hook
`pytest_unconfigure`).

Como a decisão de qual versão de Python é o padrão do projeto não é
exclusiva de Felipe (afeta CI/Docker, que são do Caike, e a decisão de
ambiente, da ADR-001, que é do Vitor), o `pyproject.toml` não foi alterado
nesta auditoria — mas a validação acima fica registrada para alinhamento da
equipe, caso a questão seja levantada.

**Confiança nesta análise:** 0,92 (alta). Fato verificável: os números de
teste, os diffs de schema (código de resposta HTTP e schema SQL) e o
comportamento runtime, nas duas versões de Python, foram todos executados e
observados diretamente, não estimados. O que seria estimativa — se o
comportamento em Windows seria idêntico — foi removido do relatório; não é
afirmado aqui.
