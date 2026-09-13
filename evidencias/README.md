# Evidências da Entrega

Esta pasta reúne os registros visuais da organização do projeto, da integração no GitHub, da documentação Swagger e da validação funcional da API de gerenciamento de tarefas.

## Evidências de organização e integração

| Arquivo | Descrição | Situação |
|---|---|---|
| `01-project-organizado.png` | GitHub Project com as Issues e os status da equipe. | Capturado |
| `02-pull-requests-integrados.png` | Pull Requests integrados da especificação, implementação, documentação, testes, Docker e CI. | Capturado |
| `03-actions-aprovado.png` | Execuções aprovadas do GitHub Actions. | Capturado |

## Evidências da documentação e da API

| Arquivo | Descrição | Situação |
|---|---|---|
| `04-swagger-quatro-rotas.png` | Página Swagger mostrando as quatro rotas da API. | Capturado |
| `05-post-criacao.png` | Criação de uma tarefa pelo `POST /tarefas`, com resposta `201`. | Capturado |
| `06-get-listagem.png` | Listagem da tarefa pelo `GET /tarefas`, com resposta `200`. | Capturado |
| `07-patch-requisicao.png` | Requisição `PATCH /tarefas/{id}` para concluir a tarefa. | Capturado |
| `07-patch-resposta-200.png` | Resposta `200` do PATCH com `concluida: true`. | Capturado |
| `08-delete-exclusao.png` | Exclusão da tarefa pelo `DELETE /tarefas/{id}`, com resposta `204`. | Capturado |
| `09-get-apos-exclusao.png` | Novo `GET /tarefas` retornando lista vazia após a exclusão. | Capturado |
| `10-erro-422.png` | Validação de entrada inválida, com resposta `422`. | Capturado |
| `11-erro-404.png` | Tentativa de operar sobre uma tarefa inexistente, com resposta `404`. | Capturado |

## Fluxo funcional validado

A sequência demonstrada nas evidências foi:

```text
POST → GET → PATCH → DELETE → GET novamente
