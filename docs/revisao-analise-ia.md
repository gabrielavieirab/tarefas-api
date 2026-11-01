# Revisão técnica da análise de IA

Registro histórico da revisão assistida de 15/10/2026.

Objeto: [PR #18](https://github.com/gabrielavieirab/tarefas-api/pull/18),
integrado em `develop` no commit `1b6294a` durante esta conferência.
O conteúdo analisado é o de `docs/analise-critica-ia.md` e
`docs/governanca-entrega2.md` no commit
[`bed7795`](https://github.com/gabrielavieirab/tarefas-api/commit/bed7795f9b0e27639f25de1f93d5efad495616c2).
O parecer registra a análise assistida; a aprovação humana é registrada no PR.

## Parecer

A estrutura cobre os temas pedidos: alucinação, código inseguro ou destrutivo,
privacidade, propriedade intelectual e revisão humana no fluxo SDD. A governança
também descreve responsáveis, branches, PRs e critérios de integração compatíveis
com o trabalho do grupo.

O texto serve como base, mas a análise comparativa ainda precisa ser preenchida
com experiências ou avaliações identificáveis antes da consolidação do relatório.
As pendências abaixo não impedem a integração da estrutura documental já feita;
precisam ser tratadas para apresentar o conteúdo como análise final da entrega 2.

## Ajustes necessários para a versão final

1. **Preencher a comparação com dados reais.** As
   [seções de ferramentas e matriz](https://github.com/gabrielavieirab/tarefas-api/blob/bed7795f9b0e27639f25de1f93d5efad495616c2/docs/analise-critica-ia.md#L25)
   ainda contêm `[Sim/Não]`, `[Nome]`, `[Avaliação]` e `[Ferramenta 1]`.
   Registrar ferramenta, finalidade, integrante, tarefa avaliada, resultado
   observado e revisão necessária. Distinguir uso no projeto de pesquisa ou
   avaliação; não atribuir uso de ferramentas aos colegas sem confirmação.

2. **Relacionar benefícios e limitações a situações do projeto.** A
   [avaliação das ferramentas](https://github.com/gabrielavieirab/tarefas-api/blob/bed7795f9b0e27639f25de1f93d5efad495616c2/docs/analise-critica-ia.md#L97)
   ainda traz instruções para preencher o texto. O item de benefícios lista
   possibilidades, sem medir resultados. Os registros verificáveis
   abaixo podem ser incorporados à avaliação das ferramentas.

3. **Fundamentar os pontos éticos e técnicos.** Incluir fontes primárias
   identificadas para as afirmações sobre tratamento de dados, limitações
   dos agentes e licenças, e associá-las ao que foi utilizado ou avaliado.
   A [seção de propriedade intelectual](https://github.com/gabrielavieirab/tarefas-api/blob/bed7795f9b0e27639f25de1f93d5efad495616c2/docs/analise-critica-ia.md#L363)
   enumera cuidados, mas ainda não apresenta essas referências. Evitar concluir
   que todo código gerado é livre de restrições ou que houve incidente de
   vazamento sem evidência. Este parecer não emite uma conclusão jurídica.

4. **Distinguir revisão humana de automação.** O fluxo proposto está adequado,
   mas afirmações como "toda sugestão foi revisada" precisam de evidências.
   A CI aprovada não substitui review. Na verificação anterior dos PRs #12 e
   #15 não havia reviews formais; o PR #16 possui
   [aprovação registrada de Caike](https://github.com/gabrielavieirab/tarefas-api/pull/16#pullrequestreview-5188617537).
   Registrar o que aconteceu e separar a regra de governança da sua comprovação.

5. **Corrigir a renderização do Markdown.** Os dois arquivos têm marcadores
   escapados, como `\#`, `\##`, `\-` e `\*\*`, além de muitas linhas vazias.
   Isso transforma títulos e listas em texto literal. O modelo de descrição
   de PR na governança usa um bloco de três crases contendo outro bloco de
   três crases; usar quatro crases no bloco externo. Conferir a renderização
   antes de converter o texto para PDF. Na análise, corrigir também
   "a IA pode apoiar ou apoiar" para "a IA pode apoiar".

## Registros verificáveis de uso de IA

**Ferramenta observada:** Codex, aplicativo desktop, na sessão de preparação
da documentação da entrega 2. Esse registro não comprova uso de Codex CLI,
Claude Code, Cursor ou Antigravity em outras atividades do projeto.

**Finalidade:** leitura dos materiais, conferência da especificação contra o
código integrado, atualização de README e ADRs, diagrama da arquitetura,
rastreabilidade dos refinamentos e execução de comandos de verificação.

**Resultados verificáveis:** documentação alinhada ao código e ao histórico
do GitHub, 80 testes locais aprovados, `pip check` aprovado, links locais
conferidos e distinção entre o contrato estático e o OpenAPI gerado. A
execução de CI citada nas evidências pertence à base publicada, não foi
executada pela ferramenta como consequência da redação do texto.

**Limitações observadas:** a ferramenta precisa de contexto e de execução
real para sustentar afirmações sobre o projeto. A documentação anterior
continha descrições desatualizadas, e a revisão identificou que o Swagger
não expõe todas as restrições aplicadas pelo código. Não foi determinada a
origem dessas diferenças nem atribuída sua criação a IA. Não houve comparação
experimental ou medição de tempo que sustente percentuais de ganho.

**Revisão necessária:** conferir fatos e resultados, preservar o escopo,
registrar limites do ambiente e obter a avaliação humana prevista no PR.
O diff, os testes e os documentos são materiais para essa avaliação, não
uma aprovação automática da contribuição.

## Encaminhamento para a consolidação

O histórico técnico está registrado em
[Relato técnico](relato-tecnico-entrega2.md). Gabriela pode incorporar as
informações factuais acima à análise e reunir as experiências dos demais.
A nova versão da comparação, suas referências e o PDF consolidado devem
ser conferidos quando estiverem disponíveis. A revisão assistida da versão
`bed7795` está registrada; a homologação humana do conteúdo final continua
uma etapa própria da equipe.
