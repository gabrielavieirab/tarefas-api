# Relato técnico — evolução da especificação

Registro histórico da entrega 2, de 15/10/2026.
Texto preparado a partir dos documentos, commits e execuções do projeto para
compor a seção de comunicação técnica do relatório consolidado.

## Desenvolvimento e colaboração

A especificação definiu o comportamento da API:
quatro operações HTTP, uma lista compartilhada e tarefas com `id`, `titulo`
e `concluida`. O trabalho detalhou entradas válidas, retornos de erro,
persistência e critérios de aceitação antes da integração da aplicação.
Isso forneceu uma referência comum para a implementação, os testes e o ambiente. A especificação foi integrada pelo
[PR #12](https://github.com/gabrielavieirab/tarefas-api/pull/12), a aplicação
pelo [PR #14](https://github.com/gabrielavieirab/tarefas-api/pull/14) e os testes
e o ambiente pelo [PR #15](https://github.com/gabrielavieirab/tarefas-api/pull/15).

Um refinamento concreto foi permitir a edição do título pelo mesmo PATCH
usado para concluir tarefas. A regra passou a distinguir campo omitido de
`null` e a preservar o estado concluído ao editar somente o texto. A mudança
foi refletida na especificação, no contrato estático e nos critérios antes
de orientar implementação e testes. O registro está em
[REF-06](refinamentos.md), e os cenários correspondentes são CA-27 a CA-31.

## Aprendizados demonstrados na etapa 2

A consolidação mostrou que documentação também precisa acompanhar a integração.
Alguns arquivos ainda descreviam a aplicação e os testes como trabalho futuro,
embora já estivessem publicados. O README também precisava explicar os comandos
de execução, o volume Docker e o comportamento exato do PATCH. A revisão
substituiu essas descrições pelo estado verificável do código e vinculou as
afirmações aos PRs e às execuções. O histórico de setembro foi preservado como
histórico, sem apresentá-lo como resultado atual.

Outro ponto foi separar resultado de teste, configuração de ambiente e aprovação
humana. Em 15/10/2026, a suíte local teve 80 testes aprovados. A execução pública
da `main` também aprovou testes no runner e no container. Esses resultados
comprovam os cenários executados, mas não significam cobertura total do código
nem aprovação dos colegas. O Python local foi 3.12.6, enquanto Docker e CI usam
3.12.10; registrar essa diferença evita afirmar que os ambientes são idênticos.

## Defesa das decisões técnicas

FastAPI e Pydantic concentram validação e serialização em modelos próximos do
contrato. SQLite permite persistir a lista sem operar um servidor de banco,
e SQLAlchemy reúne consultas e transações em um módulo pequeno. A escolha
atende à demonstração acadêmica de uma aplicação e uma tabela, com o custo
de aprender o ciclo de sessão e de manter regras de validação explícitas.

A revisão também identificou limites que precisam acompanhar a defesa: as
dependências transitivas não têm lock completo; a persistência de um volume
entre containers exige uma conferência operacional; e o OpenAPI gerado ainda
não expressa todas as regras aplicadas pelos validadores. Esses pontos foram
documentados, preservando os testes e o comportamento especificado.
As justificativas e alternativas estão nos [ADRs](decisoes_tecnicas.md).

## Uso de IA e responsabilidade pela entrega

Nesta atualização, o Codex no aplicativo desktop apoiou a leitura dos materiais,
a conferência do repositório, a redação técnica e a execução de verificações.
As evidências são os arquivos produzidos, o diff e os resultados de comandos;
não foi feita medição de economia de tempo nem comparação experimental entre
ferramentas. A [revisão da análise de IA](revisao-analise-ia.md) registra essa
contribuição e os pontos que ainda precisam ser consolidados pela equipe.

A experiência técnica descrita sustenta um fluxo em que a especificação orienta
o trabalho, os testes verificam o comportamento e o PR permite discutir a mudança.
O texto e as sugestões de IA precisam passar pela avaliação dos integrantes.
A conferência de Felipe, a revisão de clareza por Gabriela e a revisão do PDF
final são etapas distintas da preparação desta contribuição.

## Evidências para a consolidação

- [Issue #22](https://github.com/gabrielavieirab/tarefas-api/issues/22): escopo da documentação técnica.
- [PR #25](https://github.com/gabrielavieirab/tarefas-api/pull/25): publicação desta contribuição para revisão.
- [Critérios de aceitação](criterios_aceitacao.md): relação entre regras e cenários.
- [Refinamentos](refinamentos.md): evolução e decisões rastreadas.
- [Evidências de testes e CI](evidencias_testes.md): ambientes, resultados e limitações.
- [Execução pública da main](https://github.com/gabrielavieirab/tarefas-api/actions/runs/38781864191): validação de `8ecaf5f`.
