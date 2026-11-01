# Critérios de aceitação

Versão 1.1.0, vinculada à [especificação SDD](especificacao_sdd.md).
Atualização documental: 27/10/2026. Os critérios orientaram a implementação
da API por Felipe e a consolidação dos testes por Caike; o comportamento
esperado permanece o mesmo na Entrega Final.

Estes são **cenários especificados**. Os resultados das execuções estão em
[Evidências de testes e CI](evidencias_testes.md): 81 testes aprovados na
verificação local de 27/10/2026 e CI da base `668faae` aprovada, incluindo container.
O caso explícito `test_ca14_corpo_json_vazio_e_rejeitado` foi acrescentado pelo
PR #26; reforça o CA-14 existente, sem criar novo critério ou regra.
Usar banco limpo por teste e IDs retornados pelo cadastro; não depender de IDs fixos.
Quando o cenário precisar de tarefa concluída, prepará-la por uma requisição válida.

## Cadastro

- **CA-01 - Cadastro válido (RF-01, RN-01).** Dado um banco vazio, ao enviar
  `{"titulo":"Estudar"}`, esperar `201`, ID inteiro positivo, título `Estudar` e
  `concluida=false`. O GET seguinte deve conter a mesma tarefa.
- **CA-02 - Normalização (RN-03).** Enviar `{"titulo":"  Revisar API  "}`;
  esperar `201` e título persistido `Revisar API`. Preservar espaços internos
  (por exemplo, `Revisar  API`) e acentos.
- **CA-03 - Título ausente/vazio (RF-05, RN-02).** Testar separadamente `{}`,
  `{"titulo":""}`, `{"titulo":"   "}` e somente tabulações/quebras de linha.
  Esperar `422` com erro associado ao título e nenhum cadastro.
- **CA-04 - Tipo inválido (RN-02).** Para `titulo`, testar `null`, `123`, `true`,
  lista e objeto. Todos devem retornar `422`, sem converter o valor em string.
- **CA-05 - Limites do título (RN-03).** Aceitar 1 e 120 caracteres após a
  normalização; rejeitar 121 com `422`. Aceitar 120 caracteres cercados por espaços,
  persistindo só os 120 caracteres. A contagem não depende do tamanho em bytes.
- **CA-06 - Campos controlados pelo servidor (RN-04).** Enviar um título válido
  acompanhado, em casos separados, de `id`, `concluida` ou `prioridade`.
  Esperar `422`, erro no campo extra e nenhum cadastro.
- **CA-07 - Títulos repetidos (RN-03).** Cadastrar duas vezes o mesmo título;
  esperar dois `201` e IDs diferentes. Não deduplicar silenciosamente.
- **CA-08 - Corpo ausente ou JSON malformado (RF-05).** POST sem corpo ou com
  JSON incompleto e cabeçalho JSON retorna `422`; verificar que o banco permanece vazio.

## Listagem

- **CA-09 - Lista vazia (RF-02).** Em banco vazio, GET retorna `200` e exatamente `[]`.
- **CA-10 - Lista com estados diferentes (RF-02, RN-10).** Cadastrar tarefas e
  concluir uma. GET retorna todas, em ordem crescente de ID, preservando os estados
  e expondo apenas `id`, `titulo` e `concluida` por item.
- **CA-11 - Leitura sem alteração (RN-10).** Repetir o GET sem outras operações
  retorna os mesmos registros e estados.

## Conclusão

- **CA-12 - Concluir pendente (RF-03).** PATCH com `{"concluida":true}` sobre
  tarefa pendente retorna `200`, mesmo ID e título e `concluida=true`. O GET confirma.
- **CA-13 - Repetir conclusão (RN-06).** Aplicar duas vezes o PATCH válido;
  esperar `200` nas duas chamadas, mesma representação e apenas um registro.
- **CA-14 - Corpo de conclusão inválido (RN-05).** Testar ausência de corpo,
  `{}`, JSON malformado e, para `concluida`, `false`, `null`, `1`, `0`, `"true"`,
  `"false"`, lista e objeto. Esperar `422` e tarefa original inalterada.
- **CA-15 - Alterações fora do escopo (RN-05).** Acrescentar `id`, `prioridade` ou
  outro campo não permitido ao PATCH válido retorna `422`; não concluir nem editar
  o registro. `titulo` é um campo permitido desde a versão 1.1.0.
- **CA-16 - Conclusão de ID inexistente (RF-06).** Com ID válido ausente e corpo
  válido, esperar `404` e `{"detail":"Tarefa não encontrada."}`.
- **CA-17 - Validação antes da consulta (RN-09).** Com ID válido inexistente e
  corpo inválido, esperar `422`, não `404`. Cobrir tanto título inválido quanto
  conclusão inválida, inclusive quando enviados junto de outro campo válido.

## Exclusão e IDs

- **CA-18 - Exclusão (RF-04, RN-07).** Excluir tarefa pendente retorna `204` e
  zero bytes de corpo; GET não contém o ID. Repetir em cenário independente com
  tarefa concluída, obtendo o mesmo resultado.
- **CA-19 - Exclusão de ID inexistente (RF-06).** DELETE de ID válido ausente
  retorna `404` e a mensagem definida. Outros registros permanecem intactos.
- **CA-20 - Repetir exclusão (RN-07).** Excluir e repetir antes de qualquer
  novo cadastro: primeira chamada `204`; segunda `404`. O registro segue ausente.
- **CA-21 - ID inválido (RN-08).** Em PATCH (com corpo válido) e DELETE, testar
  `abc`, `1.5`, `0`, `-1` e `9223372036854775808`. Esperar `422` com erro associado
  a `path/id`; não alterar nenhum registro.
- **CA-22 - Limite válido de ID (RN-08).** Em banco vazio, usar
  `9223372036854775807` em PATCH válido e DELETE: esperar `404`, sem erro de
  conversão ou estouro do banco.

## Persistência, contrato e integração

- **CA-23 - Reinicialização (RF-07, RN-11).** Cadastrar três tarefas, editar o
  título de uma, concluir outra e excluir a terceira. Encerrar a aplicação,
  criar nova instância com o mesmo arquivo SQLite e verificar pelo GET que restam
  só as duas esperadas, com os títulos e estados corretos. Pode ser teste
  automatizado com arquivo temporário persistente entre instâncias; registrar
  também a execução no ambiente padronizado.
- **CA-24 - Isolamento (RNF-02).** A suíte usa banco temporário limpo, não lê nem
  altera o banco de uso manual e deixa a dependência de sessão restaurada ao final.
- **CA-25 - Formato das respostas (RNF-03).** Respostas `200`, `201`, `404` e `422`
  possuem JSON e seu tipo de conteúdo. `204` tem corpo vazio. Em `422`, `detail` é
  lista não vazia e cada erro tem `loc`, `msg` e `type`; tolerar campos adicionais.
- **CA-26 - Execução integrada (RNF-01, RNF-06).** A suíte completa é executada
  localmente e no container com os comandos documentados. O workflow executa a
  suíte nos PRs e integrações acordados. Guardar logs/prints com comando, resultado
  e referência da versão testada; não registrar aprovação sem uma execução real.

## Edição do texto

- **CA-27 - Editar tarefa pendente (RF-08, RN-12).** Cadastrar `Estudar matematca`
  e enviar PATCH com `{"titulo":"Estudar matemática"}`. Esperar `200`, mesmo ID,
  novo título e `concluida=false`. GET confirma; não criar uma segunda tarefa nem
  alterar outras tarefas. Repetir o PATCH retorna os mesmos dados. Substituir o
  título completo por `Revisar português` também é válido.
- **CA-28 - Editar tarefa concluída (RF-08, RN-12).** Concluir uma tarefa e editar
  apenas seu título. Esperar `200`, mesmo ID, novo título e `concluida=true` no
  retorno e no GET. A edição não reabre a tarefa.
- **CA-29 - Validar título na edição (RF-05, RF-08, RN-02/RN-03).** No PATCH,
  aceitar títulos de 1 e 120 caracteres, normalizar espaços nas extremidades e
  preservar espaços internos e acentos, como no POST. Aceitar título já usado por
  outra tarefa. Rejeitar vazio, só espaços, 121 caracteres após normalização,
  `null`, número, booleano, lista e objeto com `422`, mantendo a tarefa original.
- **CA-30 - Editar e concluir juntos (RF-03, RF-08, RN-12).** PATCH de tarefa
  pendente com `{"titulo":"Revisar português","concluida":true}` retorna `200`,
  mesmo ID, novo texto e estado concluído; GET confirma ambos. Em casos separados,
  enviar título inválido com `true` e título válido com conclusão inválida:
  esperar `422` e nenhum dos campos alterados.
- **CA-31 - Editar ID inexistente (RF-06, RF-08).** Com ID válido ausente e título
  válido, esperar `404` e `{"detail":"Tarefa não encontrada."}`. Não criar uma
  tarefa; preservar os demais registros.

## Rastreabilidade e revisão da Entrega Final

- CA-01 a CA-22, CA-25 e CA-27 a CA-31: cenários em `tests/test_tarefas.py`.
- CA-23: `test_rf07_persistencia_entre_reinicializacoes`, com dois processos
  usando o mesmo SQLite temporário.
- CA-24: `tests/test_isolamento.py::test_ca24_banco_manual_e_limpeza`,
  em [test_isolamento.py](../tests/test_isolamento.py), parametrizado com e sem
  `TAREFAS_DATABASE_URL`. Verifica que o banco manual não é acessado nem alterado,
  os bancos temporários são removidos e a dependência de sessão é restaurada.
  A preparação e a limpeza ficam em [conftest.py](../tests/conftest.py).
- CA-26: execução local documentada e
  [CI da develop](https://github.com/gabrielavieirab/tarefas-api/actions/runs/40586231416),
  com testes no runner, build e testes no container aprovados. A conferência
  operacional da persistência do volume Docker segue com Caike.

A especificação foi integrada pelo
[PR #12](https://github.com/gabrielavieirab/tarefas-api/pull/12), e as
[Issues #1](https://github.com/gabrielavieirab/tarefas-api/issues/1) e
[#9](https://github.com/gabrielavieirab/tarefas-api/issues/9) estão fechadas.
Isso comprova o estado da integração, sem substituir uma evidência específica
de revisão ou aprovação por cada colega.

Na revisão documental final, Felipe confere a aderência ao código,
Gabriela confere a clareza e Caike confere os comandos e evidências de ambiente.
Novos comentários e decisões devem ser registrados em
[Refinamentos](refinamentos.md), com os links correspondentes.
