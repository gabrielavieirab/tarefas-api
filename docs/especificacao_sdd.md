# Especificação SDD - API de lista de tarefas

Eu, Vitor (@vitorborges10), sou o responsável por esta especificação.

**Versão do contrato:** 1.1.0, de 05/09/2026.
**Atualização documental:** 15/10/2026, para a entrega 2.

**Estado:** contrato implementado na base `8ecaf5f` da `main`, com suíte de
80 testes aprovada. A consolidação documental da entrega 2 aguarda revisão
dos colegas; não há alteração de comportamento nesta atualização.

**Rastreabilidade:** [Issue #1](https://github.com/gabrielavieirab/tarefas-api/issues/1).
Consolidação da entrega 2: [Issue #22](https://github.com/gabrielavieirab/tarefas-api/issues/22).

## 1. Problema e objetivo

Uma pessoa precisa registrar pequenas atividades, consultar o que foi cadastrado,
editar o texto de uma tarefa, identificar atividades concluídas e remover registros
que não deseja manter.
Anotações dispersas dificultam manter uma lista com estado consistente.

A solução é uma API HTTP que centraliza essa lista e persiste os registros entre
execuções. O consumidor pode ser a documentação interativa da API ou outro cliente
HTTP. A entrega inicial demonstra um ciclo pequeno e completo: especificar,
implementar, testar e revisar colaborativamente.

SDD (Spec-Driven Development) significa que o comportamento é descrito e revisado
antes de orientar a geração de código, a implementação e os testes.

## 2. Escopo funcional mantido na entrega 2

Inclui exatamente quatro operações HTTP: cadastrar, listar, atualizar e excluir
tarefas. A atualização permite editar o texto (`titulo`), marcar como concluída
ou fazer ambas as alterações na mesma requisição. Cada tarefa tem `id`, `titulo`
e `concluida`, em uma única tabela.
Todas as tarefas pertencem à mesma lista compartilhada; não há conceito de usuário.

Não fazem parte desta versão: interface própria, autenticação, usuários, categorias,
prioridades, datas, paginação, filtros, reabertura de tarefa,
consulta individual por GET, relacionamentos e cálculos. A página de documentação
automática do FastAPI é uma ferramenta de apoio, não uma quinta operação de negócio.

O fluxo de GitHub, as instruções de IA, o ambiente, a suíte e as evidências continuam
fazendo parte da entrega do grupo. Na entrega 2, a equipe consolida a implementação,
o refinamento por testes, a governança, a defesa técnica e a análise de IA.
O contrato funcional permanece o da versão 1.1.0; esses trabalhos não acrescentam
rotas, campos ou regras de negócio.

## 3. Tecnologias e decisões

Adotar Python 3.12, FastAPI, Pydantic 2, Uvicorn, SQLAlchemy 2 e SQLite, com acesso
síncrono ao banco. Para validação, usar pytest, TestClient do FastAPI e HTTPX.
Padronizar o ambiente com `venv`/pip, `pyproject.toml` e Docker; executar a suíte
também no GitHub Actions.

As dependências diretas estão fixadas em `pyproject.toml`: FastAPI 0.141.1,
Uvicorn 0.52.4, Pydantic 2.13.5, SQLAlchemy 2.0.52, pytest 9.1.1 e HTTPX 0.28.1.
O Docker usa `python:3.12.10-slim` e o CI configura Python 3.12.10.
Ainda não há lock das dependências transitivas nem digest da imagem; o
[ADR-004](decisoes_tecnicas.md) registra esse limite da reprodução do ambiente.
As execuções efetivamente realizadas estão em
[Evidências de testes e CI](evidencias_testes.md).

As justificativas e a decomposição dos componentes estão em
[Decisões técnicas](decisoes_tecnicas.md).

## 4. Requisitos funcionais

- **RF-01 - Cadastrar:** receber um título válido, gerar um ID, salvar a tarefa
  com `concluida=false` e retornar a representação persistida com HTTP `201`.
- **RF-02 - Listar:** retornar todas as tarefas persistidas com HTTP `200`, em
  ordem crescente de ID. Sem registros, retornar `[]`.
- **RF-03 - Concluir:** receber `{"concluida": true}`, atualizar uma tarefa
  existente e retornar sua representação com HTTP `200`. Repetir mantém o estado.
- **RF-04 - Excluir:** remover fisicamente uma tarefa existente e retornar HTTP
  `204`, sem corpo de resposta.
- **RF-05 - Rejeitar entradas inválidas:** retornar HTTP `422` e detalhes da
  validação, sem alterar dados.
- **RF-06 - Informar ausência:** para um ID válido sem registro correspondente,
  PATCH e DELETE retornam HTTP `404` e a mensagem definida no contrato.
- **RF-07 - Persistir:** cadastros, edições, conclusões e exclusões confirmados devem
  continuar refletidos após reiniciar a aplicação com o mesmo arquivo de banco.
- **RF-08 - Editar:** receber um novo `titulo` válido em PATCH, atualizar o texto
  da tarefa existente e retornar sua representação com HTTP `200`. Preservar o ID
  e os campos omitidos; editar o texto de uma tarefa concluída não a reabre.

## 5. Requisitos não funcionais

- **RNF-01 - Reprodutibilidade:** instalação documentada, Python 3.12 em ambiente
  local, container e CI, com dependências compatíveis e versões fixadas no processo
  de ambiente. O container deve executar a mesma aplicação e suíte do projeto.
- **RNF-02 - Testabilidade:** banco de testes isolado do banco de uso manual;
  cenários independentes e execução por `pytest`. A dependência da sessão do banco
  deve poder ser substituída nos testes.
- **RNF-03 - Contrato consistente:** JSON nas entradas de POST/PATCH e nas
  respostas com conteúdo; `Content-Type: application/json`. A resposta `204` não
  carrega JSON nem qualquer outro corpo. Rotas públicas usam os nomes combinados.
- **RNF-04 - Manutenção:** separar validação/serialização, rotas, persistência e
  configuração de banco em módulos pequenos, sem frameworks arquiteturais extras.
- **RNF-05 - Integridade:** confirmar alterações no banco antes de responder
  sucesso; falhas de validação não podem criar, editar, concluir ou excluir registros.
- **RNF-06 - Rastreabilidade:** associar a implementação aos RFs e aos critérios
  de aceitação; registrar decisões, revisões reais e mudanças da especificação.
- **RNF-07 - Documentação verificável:** o contrato e a documentação automática
  devem descrever o comportamento implementado. Relatórios distinguem cenários
  planejados de testes efetivamente executados.

O alvo é uma demonstração acadêmica local com poucos registros e um processo da
API. Não foi estabelecido requisito de alta concorrência ou SLA de desempenho.

## 6. Modelo de dados

Tabela de domínio: `tarefas`.

- **`id`:** inteiro positivo gerado pelo banco, chave primária e não nulo. A API
  aceita IDs até `9223372036854775807` (limite de inteiro assinado de 64 bits).
  O consumidor não escolhe nem altera esse campo. IDs dos exemplos são ilustrativos;
  não se exige numeração sem lacunas nem que o primeiro ID de qualquer ambiente seja 1.
- **`titulo`:** texto obrigatório e não nulo, com 1 a 120 caracteres após remover
  espaços em branco das extremidades. Manter acentos, maiúsculas, minúsculas e
  espaços internos. A contagem usa caracteres Unicode, não bytes.
- **`concluida`:** booleano não nulo, inicialmente `false`. Na API, usar booleanos
  JSON; na tabela SQLite, o mapeamento booleano pode usar `0` e `1`.

No modelo SQLAlchemy, usar tipos equivalentes a `Integer`, `String(120)` e `Boolean`.
A validação do limite do título é responsabilidade da aplicação: declarar apenas
`String(120)` no SQLite não substitui essa validação.

## 7. Regras de negócio e validação

- **RN-01:** toda tarefa nasce pendente (`concluida=false`).
- **RN-02:** o título deve ser uma string JSON. `null`, número, booleano, objeto,
  lista, string vazia e texto composto só por espaços são inválidos. O campo é
  obrigatório no POST; no PATCH, sua ausência mantém o título atual.
- **RN-03:** remover espaços em branco das extremidades antes de verificar o
  limite de 1 a 120 caracteres. Títulos iguais são permitidos; no cadastro,
  geram tarefas distintas, enquanto a edição mantém o ID da tarefa alterada.
- **RN-04:** POST aceita apenas `titulo`. Campos extras, inclusive `id` e
  `concluida`, retornam `422`, evitando sobrescrita de campos controlados pelo servidor.
- **RN-05:** PATCH exige corpo JSON com pelo menos um dos campos `titulo` e
  `concluida`. Aceitar um ou ambos. Quando presente, `titulo` segue RN-02/RN-03;
  `concluida` aceita somente o booleano `true`, rejeitando `false`, `1`, `"true"`
  e `null`. Corpo vazio `{}`, corpo ausente e campos extras, inclusive `id`,
  retornam `422`. Não há reabertura nesta versão.
- **RN-06:** enviar apenas `{"concluida":true}` para uma tarefa já concluída retorna
  `200` e a mesma representação, mantendo ID e título. É uma operação idempotente
  quanto ao estado.
- **RN-07:** excluir remove o registro da lista e do banco. Uma nova exclusão do
  mesmo ID, ainda ausente, retorna `404`.
- **RN-08:** o ID da rota deve representar um inteiro positivo dentro do limite
  definido. Texto não numérico, fração, zero, negativo e valor acima do limite
  retornam `422`. IDs válidos inexistentes retornam `404`.
- **RN-09:** validar a entrada antes de procurar o registro. Em PATCH com ID
  inexistente e corpo inválido, retornar `422`. Não se exige ordem específica
  dos itens quando houver mais de um erro de validação.
- **RN-10:** o GET lista pendentes e concluídas, sem filtros nem paginação, em
  ordem crescente de ID. A listagem não altera os registros.
- **RN-11:** o arquivo SQLite deve ser reutilizado entre reinicializações. Testes
  não devem abrir ou apagar esse arquivo. No Docker, montar um volume no diretório
  de dados para preservar os registros ao recriar o container.
- **RN-12:** PATCH altera apenas os campos enviados e mantém o ID. Editar somente
  o título preserva o estado pendente ou concluído; concluir sem enviar título
  preserva o texto. A edição pode corrigir uma palavra ou substituir todo o texto.
  Validar todos os campos antes de salvar; se um for inválido, nenhum é alterado.
  Repetir a mesma atualização válida, sem mudanças intermediárias, retorna `200`
  e mantém os mesmos dados. A edição não cria outra tarefa nem altera outras linhas.

## 8. Contratos HTTP

Endereço local: `http://127.0.0.1:8000`, após iniciar a aplicação com os comandos
do [README](../README.md). A documentação Swagger fica em `/docs`.
As rotas canônicas não têm barra final.

### POST /tarefas

Corpo obrigatório, `Content-Type: application/json`:

```json
{"titulo": "  Estudar para o bootcamp  "}
```

Resposta `201 Created`:

```json
{"id": 1, "titulo": "Estudar para o bootcamp", "concluida": false}
```

O registro retornado já deve estar persistido. Título inválido, corpo ausente,
JSON malformado ou campo extra retornam `422`. Nenhum registro é criado nesses casos.

### GET /tarefas

Sem corpo e sem parâmetros de consulta definidos nesta versão.

Resposta `200 OK`:

```json
[
  {"id": 1, "titulo": "Estudar para o bootcamp", "concluida": false},
  {"id": 2, "titulo": "Revisar a especificação", "concluida": true}
]
```

Sem registros, a resposta é `200 OK` com `[]`, não `404`.

### PATCH /tarefas/{id}

Exemplo: `PATCH /tarefas/1`. Corpo obrigatório, `Content-Type: application/json`.
Enviar pelo menos um dos campos aceitos.

**Editar o texto:** para trocar `Estudar matematca` por `Estudar matemática`:

```json
{"titulo": "Estudar matemática"}
```

Resposta `200 OK`, supondo que a tarefa estava pendente:

```json
{"id": 1, "titulo": "Estudar matemática", "concluida": false}
```

O novo texto também pode descrever outra atividade, como `Revisar português`.
Se a tarefa já estava concluída, editar só o título mantém `concluida=true`.

**Marcar como concluída**, preservando o título atual:

```json
{"concluida": true}
```

Resposta `200 OK`:

```json
{"id": 1, "titulo": "Estudar matemática", "concluida": true}
```

**Editar e concluir na mesma requisição:**

```json
{"titulo": "Revisar português", "concluida": true}
```

Resposta `200 OK`:

```json
{"id": 1, "titulo": "Revisar português", "concluida": true}
```

O GET posterior deve refletir as alterações persistidas. Repetir uma requisição
válida, sem alterações intermediárias, retorna `200` com os mesmos dados.
ID válido inexistente retorna `404`; ID ou corpo inválido retorna `422`.
Por exemplo, `{"titulo":"","concluida":true}` retorna `422` sem editar nem concluir.

### DELETE /tarefas/{id}

Exemplo: `DELETE /tarefas/1`. Sem corpo de requisição.

Resposta `204 No Content`, com corpo de comprimento zero. Não retornar `{}`,
`null` ou mensagem de sucesso. Uma listagem posterior não deve conter o registro.
ID válido inexistente retorna `404`; ID inválido retorna `422`.

### Erros

**404 - Tarefa inexistente**, em PATCH/DELETE com entrada válida:

```json
{"detail": "Tarefa não encontrada."}
```

**422 - Validação**, exemplo ilustrativo de título ausente:

```json
{
  "detail": [
    {"loc": ["body", "titulo"], "msg": "Field required", "type": "missing"}
  ]
}
```

Manter a estrutura de validação do FastAPI: `detail` é uma lista não vazia de
itens com `loc`, `msg` e `type`. Campos adicionais, como `input` e `ctx`, podem
existir. Mensagens e códigos internos podem variar conforme a versão ou o
validador; testes devem verificar status, estrutura e campo afetado, sem depender
de uma frase em inglês. JSON malformado é `422`, localizado no corpo.

Os contratos para POST/PATCH consideram clientes enviando JSON com o cabeçalho
correto. Outros tipos de mídia não são um cenário de aceitação desta versão.
Falhas inesperadas não devem ser convertidas em sucesso nem expor detalhes do banco.

## 9. Critérios de aceitação e evolução

[Critérios de aceitação](criterios_aceitacao.md) relaciona cada cenário ao requisito
ou regra correspondente. A implementação de Felipe está em `app/`; a suíte
consolidada por Caike está em `tests/`. As contribuições foram integradas pelos
[PRs #14](https://github.com/gabrielavieirab/tarefas-api/pull/14) e
[#15](https://github.com/gabrielavieirab/tarefas-api/pull/15).
A especificação e [OpenAPI estático](openapi.json) devem ser alterados
no mesmo PR sempre que um contrato mudar. A atualização de 15/10/2026 mantém
as regras e os 31 critérios de aceitação existentes.

Revisões do grupo e resultados reais dos testes devem ser registrados em
[Refinamentos](refinamentos.md), com motivo, impacto e link da evidência.
O relatório de [testes e CI](evidencias_testes.md) distingue a execução local
de 15/10/2026, a execução pública da base integrada e as limitações operacionais.

**Limitação de documentação automática:** `/openapi.json` é gerado pelo FastAPI
a partir dos esquemas e rotas. Validadores personalizados aplicam normalização,
limite do título, proibição de `null`, conclusão apenas com `true` e PATCH não
vazio, mas esses detalhes não são todos expressos no esquema gerado. As respostas
404 também não estão todas declaradas nele. O contrato estático preserva essas
regras; completar os metadados da documentação automática permanece uma pendência
de documentação em relação ao RNF-07, sem modificar o comportamento para contorná-la.
