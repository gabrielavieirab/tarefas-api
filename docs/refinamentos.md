# Registro de refinamentos da especificação

Contrato atual: 1.1.0, de 05/09/2026. Atualização documental: 15/10/2026.
Os registros diferenciam evolução de regras, integração de código e correção
de documentação; a consolidação da entrega 2 não muda o comportamento da API.

## Estado da revisão

A especificação da [Issue #1](https://github.com/gabrielavieirab/tarefas-api/issues/1)
foi integrada pelo [PR #12](https://github.com/gabrielavieirab/tarefas-api/pull/12).
A implementação, os testes e o ambiente chegaram pelos PRs #14 e #15; a entrega
inicial foi publicada em `main` pelo PR #17. As Issues #1 e
[#9](https://github.com/gabrielavieirab/tarefas-api/issues/9) estão fechadas.

Na consulta de 15/10/2026, os PRs #12 e #15 não possuem reviews formais
registrados. O merge e o fechamento de uma Issue não são tratados como prova
de aprovação individual. A documentação da entrega 2 será revisada por Felipe,
com conferência de clareza e aderência por Gabriela.

As entradas de 05/09/2026 abaixo preservam a situação da proposta naquela data.
Os registros da integração e das execuções posteriores estão na seção de 15/10/2026.

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

**Situação em 05/09/2026:** proposta para revisão no
[PR #12](https://github.com/gabrielavieirab/tarefas-api/pull/12), vinculada à Issue #1.
O estado posterior da integração está registrado em REF-07.

## 15/10/2026 - Consolidação documental da entrega 2

**REF-07 - Substituir o estado de proposta pelo estado integrado.**

**Anterior:** os documentos afirmavam que aplicação, testes e ambiente ainda
seriam produzidos. **Constatação:** o histórico contém os
[PRs #12](https://github.com/gabrielavieirab/tarefas-api/pull/12),
[#14](https://github.com/gabrielavieirab/tarefas-api/pull/14),
[#15](https://github.com/gabrielavieirab/tarefas-api/pull/15),
[#16](https://github.com/gabrielavieirab/tarefas-api/pull/16) e
[#17](https://github.com/gabrielavieirab/tarefas-api/pull/17) integrados.

**Decisão:** documentar a estrutura real de `app/`, `tests/`, Docker e CI,
tomando `8ecaf5f` como base. **Impacto:** README, especificação, arquitetura,
ADRs, critérios e guia da contribuição. Não muda RFs, regras ou respostas HTTP.
**Evidência:** código versionado, PRs e Issues #1/#9 fechadas. Aprovação humana
da nova consolidação permanece pendente; não foi inferida a partir dos merges.

**REF-08 - Relacionar a ampliação do harness aos critérios existentes.**

**Anterior:** a contribuição de implementação tinha 64 testes; o registro de
especificação ainda informava ausência de suíte. **Constatação:** o
[PR #15](https://github.com/gabrielavieirab/tarefas-api/pull/15) acrescentou
limites, asserções, isolamento do banco manual e persistência entre processos,
chegando a 80 casos.

**Decisão:** manter os 31 critérios e atualizar sua rastreabilidade para os
testes efetivos. **Impacto:** CA-23, CA-24, CA-26 e referências aos demais
cenários. Não há reespecificação para acomodar defeito nem remoção de testes.
**Verificação:** `python -m pytest tests -v --junitxml=test-results/pytest.xml`
em 15/10/2026: `80 passed, 1 warning in 9.99s`. Ambiente e limites em
[Evidências de testes e CI](evidencias_testes.md).

**REF-09 - Registrar a correção dos relatórios no CI.**

**Anterior:** a evidência local de setembro ainda deixava Docker e CI remotos
pendentes. **Constatação:** o
[commit 8ecaf5f](https://github.com/gabrielavieirab/tarefas-api/commit/8ecaf5f890ecfa4c2c4bbcefa378c03139b73e0d)
cria `test-results` no runner e monta esse diretório em `/resultados` no
container para publicar os dois XML juntos.

**Decisão:** registrar a correção de infraestrutura, sem mudar o contrato da API.
**Impacto:** evidência de CA-26, README e ADR-004.
**Verificação:** [execução 38781864191](https://github.com/gabrielavieirab/tarefas-api/actions/runs/38781864191)
da `main`, em 15/10/2026, com testes no runner, build, testes no container e
publicação de `resultados-testes` aprovados. A persistência de um volume entre
containers não é exercitada por esses passos e continua na validação operacional.

**REF-10 - Corrigir descrições ambíguas no README.**

**Anterior:** o README dizia que os IDs começavam em 1 e que PATCH alterava o
status, sem explicitar a proibição de reabertura; também faltavam os comandos
de instalação e execução, e o exemplo JSON estava sem fechamento do bloco.
**Decisão:** orientar o uso do ID retornado, descrever edição e conclusão com
`true`, completar os comandos e incluir diagramas versionados.
**Impacto:** comunicação de RN-05, RN-08, RN-12 e CA-26; nenhuma regra nova.
**Verificação:** testes de IDs, conclusão e edição já existentes, suíte aprovada
e conferência dos links e comandos documentados.

**REF-11 - Tornar explícito o limite da reprodução do ambiente.**

**Anterior:** ADR-004 previa lock também das dependências transitivas.
**Constatação:** o ambiente integrado fixa somente as dependências diretas e
Python 3.12.10 em Docker/CI, conforme o registro do PR #15.
**Decisão:** ajustar o ADR ao estado adotado e registrar a fixação completa como
melhoria a avaliar com Caike, sem alegar reprodução exata.
**Impacto:** ADR-004, seção de tecnologias da especificação e README.
**Verificação:** instalação em ambiente virtual e `python -m pip check`
aprovados em 15/10/2026; a execução local usa Python 3.12.6. O resultado do CI
com Python 3.12.10 é uma evidência separada.

**REF-12 - Distinguir contrato estático e documentação gerada.**

**Constatação:** os validadores de `app/schemas.py` impõem regras que não estão
completamente expressas no OpenAPI gerado, e as rotas não declaram nele todos
os retornos 404. **Decisão:** preservar o contrato estático 1.1.0 e registrar
o complemento desses metadados como pendência documental do RNF-07.
**Impacto:** README, especificação e ADR-003. A atualização de `docs/openapi.json`
altera apenas título e descrições de contexto; os esquemas e contratos permanecem.
**Verificação:** consulta ao esquema gerado e conferência com o contrato
estático; o comportamento de validação e 404 continua coberto pelos testes.

**REF-13 - Preparar comunicação técnica e revisão da análise de IA.**

**Constatação:** a [Issue #22](https://github.com/gabrielavieirab/tarefas-api/issues/22)
atribui a documentação técnica a Vitor. A análise de IA de Gabriela no
[PR #18](https://github.com/gabrielavieirab/tarefas-api/pull/18), integrado
em `develop` durante a conferência de 15/10/2026, ainda contém campos de modelo
na comparação de ferramentas e problemas de formatação Markdown.

**Decisão:** preparar um relato técnico apoiado no histórico e registrar uma
revisão assistida da versão `bed7795`, incluindo fatos observados na contribuição
de Vitor. Não preencher experiências dos colegas nem declarar aprovação humana
da versão final. **Impacto:** [relato técnico](relato_experiencia_vitor.md),
[parecer da análise de IA](revisao_ia_vitor.md), README e guia da contribuição.
**Evidência:** fontes e trechos identificados no parecer. A matriz final e o PDF
continuam sob consolidação de Gabriela; as regras da API não mudam.

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
