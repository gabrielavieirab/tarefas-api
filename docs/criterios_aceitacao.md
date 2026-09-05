# Critérios de aceitação

Versão 1.0.0, vinculada à [especificação SDD](especificacao_sdd.md).
Defini os critérios abaixo para orientar a implementação da API por Felipe
e os testes por Caike.

Estes são **cenários especificados**, não resultados de testes executados.
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
- **CA-15 - Alterações fora do escopo (RN-05).** Acrescentar `titulo`, `id` ou
  outro campo ao PATCH válido retorna `422`; não concluir nem alterar o registro.
- **CA-16 - Conclusão de ID inexistente (RF-06).** Com ID válido ausente e corpo
  válido, esperar `404` e `{"detail":"Tarefa não encontrada."}`.
- **CA-17 - Validação antes da consulta (RN-09).** Com ID válido inexistente e
  corpo inválido, esperar `422`, não `404`.

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

- **CA-23 - Reinicialização (RF-07, RN-11).** Cadastrar três tarefas, concluir
  uma e excluir outra. Encerrar a aplicação, criar nova instância com o mesmo
  arquivo SQLite e verificar pelo GET que restam só as duas esperadas, com os
  estados corretos. Pode ser teste automatizado com arquivo temporário persistente
  entre instâncias; registrar também a execução no ambiente padronizado.
- **CA-24 - Isolamento (RNF-02).** A suíte usa banco temporário limpo, não lê nem
  altera o banco de uso manual e deixa a dependência de sessão restaurada ao final.
- **CA-25 - Formato das respostas (RNF-03).** Respostas `200`, `201`, `404` e `422`
  possuem JSON e seu tipo de conteúdo. `204` tem corpo vazio. Em `422`, `detail` é
  lista não vazia e cada erro tem `loc`, `msg` e `type`; tolerar campos adicionais.
- **CA-26 - Execução integrada (RNF-01, RNF-06).** A suíte completa é executada
  localmente e no container com os comandos documentados. O workflow executa a
  suíte nos PRs e integrações acordados. Guardar logs/prints com comando, resultado
  e referência da versão testada; não registrar aprovação sem uma execução real.

## Revisão da especificação

- [ ] Felipe confirma que os contratos e as interfaces de persistência são implementáveis.
- [ ] Caike confirma que os cenários são testáveis no ambiente escolhido.
- [ ] O grupo valida limite do título, corpo do PATCH, regras de campos extras e códigos HTTP.
- [ ] Registrarei os comentários e ajustes em `refinamentos.md`, com links reais.

A Issue #1 deve ser considerada concluída somente após a revisão prevista nela.
Os cenários CA-01 a CA-26 serão transformados em testes/evidências nas Issues #4 a
#8; não é necessário criar uma Issue por cenário.
