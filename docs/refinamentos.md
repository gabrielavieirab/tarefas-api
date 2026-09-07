# Registro de refinamentos da especificação

Mantenho este registro de refinamentos. Versão atual: 1.1.0, de 05/09/2026.

## Estado da revisão

Preparei a proposta inicial para a [Issue #1](https://github.com/gabrielavieirab/tarefas-api/issues/1).
Revisão por Felipe e Caike: **pendente**. Testes da API e revisão de integração
da [Issue #9](https://github.com/gabrielavieirab/tarefas-api/issues/9): **pendentes
das contribuições de implementação, ambiente e testes**.

Os registros abaixo documentam a análise inicial e a evolução da minha proposta.
Não representam comentários, aprovações ou testes realizados por colegas.

## 05/09/2026 - Versão 1.0.0: definição inicial

**Entradas consultadas:** divisão acordada com o grupo, roteiro da entrega inicial,
Issues #1, #4, #5, #6, #7 e #8 e `AGENTS.md` integrado pelo
[PR #11](https://github.com/gabrielavieirab/tarefas-api/pull/11).

**REF-01 - Confirmar a base técnica existente.** As Issues e `AGENTS.md` já
mencionavam Python, FastAPI, SQLite, SQLAlchemy e pytest. A proposta mantém essa
base e documenta a escolha, acrescentando as convenções de versão e execução.
Impacto: ADR-001, ADR-002 e ADR-004; orienta Felipe e Caike.

**REF-02 - Tornar o PATCH verificável.** A operação era descrita como marcar uma
tarefa concluída, sem corpo ou repetição definidos. A proposta exige somente o
booleano `true` em `concluida`, rejeita reabertura e mantém `200` na repetição.
Impacto: RF-03, RN-05/RN-06 e CA-12 a CA-17.

**REF-03 - Precisar o título.** A regra inicial exigia título não vazio.
A proposta define tipo estrito, normalização nas extremidades, limite de 120
caracteres e títulos repetidos permitidos. Impacto: RN-02/RN-03 e CA-02 a CA-07.

**REF-04 - Alinhar erros e retorno de exclusão.** A Issue #5 já prevê `201`,
`200`, `204`, `404` e `422`. A proposta define os corpos, diferencia ID inválido
de inexistente e proíbe corpo no `204`. Impacto: contratos e CA-16 a CA-22/CA-25.

**REF-05 - Definir leitura e persistência.** A proposta determina ordem por ID,
arquivo preservado entre reinicializações e banco isolado para testes.
Impacto: RF-02/RF-07, RN-10/RN-11 e CA-09 a CA-11/CA-23/CA-24.

## 05/09/2026 - Versão 1.1.0: edição do texto da tarefa

**REF-06 - Permitir corrigir ou substituir o texto.** Identifiquei a necessidade
de alterar uma tarefa já cadastrada, por exemplo corrigir `Estudar matematca` para
`Estudar matemática` ou trocar a atividade por `Revisar português`.

Na versão 1.0.0, o PATCH aceitava apenas conclusão. Atualizei a proposta para
aceitar `titulo`, `concluida: true` ou ambos, com pelo menos um campo. A edição
preserva ID e campos omitidos, inclusive o estado concluído, e usa a validação de
título do cadastro. Um campo inválido impede toda a alteração. Permanecem quatro
operações HTTP, três campos e uma tabela.

**Impacto:** RF-07/RF-08, RN-02/RN-05/RN-12, contrato OpenAPI, ADR-003,
`TarefaAtualizar`, `atualizar_tarefa`, CA-15/CA-17/CA-23 e novos CA-27 a CA-31.
Felipe precisa considerar a edição na implementação e Caike nos testes;
Gabriela usará a versão revisada ao consolidar as instruções e a documentação.

**Situação:** proposta para revisão no
[PR #12](https://github.com/gabrielavieirab/tarefas-api/pull/12), vinculada à Issue #1.
Registrarei o feedback e a aprovação quando ocorrerem.

## Como registrar os próximos ajustes

Para cada feedback real, acrescentarei uma entrada com:

1. Data e versão da especificação.
2. Autor da revisão ou teste que revelou o problema.
3. Link do comentário no PR, Issue ou execução de teste.
4. Comportamento anterior e comportamento decidido, com motivo.
5. Requisitos, contrato OpenAPI e critérios de aceitação afetados.
6. Situação da decisão e link de aprovação, quando houver.

Se a revisão confirmar o texto sem alteração, registrarei a confirmação e seu link.
Se o teste revelar defeito na implementação, registrarei o resultado e a correção
do código; não mudarei a regra automaticamente para fazer o teste passar.
