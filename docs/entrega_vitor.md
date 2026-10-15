# Contribuição de Vitor - entrega 2

Atualização: 15/10/2026. Responsável: Vitor de Assis Patricio Borges,
RA 22304737. Branch: `codex/documentacao-entrega2`, baseada na `develop`
no commit `1b6294a`. A versão publicada da `main` consultada foi `8ecaf5f`;
as bases têm a mesma aplicação e os mesmos testes. A diferença de CI da `main`
é registrada separadamente nas evidências.

Rastreabilidade: [Issue #22](https://github.com/gabrielavieirab/tarefas-api/issues/22).
Publicação: [PR #25 para develop](https://github.com/gabrielavieirab/tarefas-api/pull/25).

## Escopo da contribuição

Consolidar a especificação, a arquitetura e a comunicação técnica da API
implementada, conforme a divisão da equipe para a etapa intermediária.
O contrato continua na versão 1.1.0: quatro operações HTTP, uma tabela,
três campos, edição de título e conclusão sem reabertura.

Materiais atualizados:

- [README](../README.md): instalação, execução, testes, Docker, rotas,
  equipe, fluxo, CI e links da documentação.
- [Arquitetura](arquitetura.md): diagrama versionado, módulos implementados,
  sessões, inicialização, persistência e isolamento dos testes.
- [Decisões técnicas](decisoes_tecnicas.md): consolidação dos ADRs de API,
  banco, validação, ambiente e governança, com defesa das escolhas e limitações.
- [Especificação SDD](especificacao_sdd.md): estado integrado e tecnologias
  efetivas, preservando requisitos e contratos existentes.
- [OpenAPI estático](openapi.json): atualização das descrições de contexto,
  sem mudança de operações, esquemas ou códigos HTTP.
- [Critérios de aceitação](criterios_aceitacao.md): vínculo dos 31 critérios
  com a suíte existente e com a execução integrada.
- [Refinamentos](refinamentos.md): integração, evolução dos testes, correção
  do CI e ajustes documentais rastreados em REF-07 a REF-12.
- [Evidências de testes](evidencias_testes.md): acréscimo da verificação de
  15/10/2026, preservando o relatório histórico de setembro.
- [Relato técnico](relato_experiencia_vitor.md): contribuição para a seção de
  aprendizados e desafios, baseada nos registros do projeto.
- [Revisão da análise de IA](revisao_ia_vitor.md): parecer assistido sobre a
  versão de Gabriela, com ajustes necessários e a contribuição factual de Vitor.

## Validação desta atualização

O pull de `main` incorporou aplicação, testes, Docker, CI e evidências da
entrega inicial. A atualização documental não altera `app/`, `tests/`,
`pyproject.toml`, Dockerfile ou workflow.

Com o ambiente virtual local:

```text
python -m pip install -e ".[test]"
python -m pip check
python -m pytest tests -v --junitxml=test-results/pytest.xml
```

Resultado em Windows com Python 3.12.6: ambiente sem dependências quebradas,
**80 testes aprovados, um aviso de descontinuação, zero falhas e zero ignorados**.
O relatório XML está em `test-results/pytest.xml`, ignorado pelo Git.

A [execução pública da main](https://github.com/gabrielavieirab/tarefas-api/actions/runs/38781864191),
com Python 3.12.10 e base `8ecaf5f`, aprovou testes no runner, build Docker,
testes no container e publicação dos relatórios. Docker não estava disponível
neste ambiente local; essa evidência remota não é apresentada como build local.
A CI da nova contribuição é acompanhada nos checks do
[PR #25](https://github.com/gabrielavieirab/tarefas-api/pull/25), separadamente
da execução histórica da `main`.

## Integração anterior e revisão

Minha contribuição inicial foi integrada pelo
[PR #12](https://github.com/gabrielavieirab/tarefas-api/pull/12).
A aplicação veio pelo [PR #14](https://github.com/gabrielavieirab/tarefas-api/pull/14),
os testes e o ambiente pelo [PR #15](https://github.com/gabrielavieirab/tarefas-api/pull/15),
as evidências pelo [PR #16](https://github.com/gabrielavieirab/tarefas-api/pull/16)
e a publicação em `main` pelo
[PR #17](https://github.com/gabrielavieirab/tarefas-api/pull/17).
As Issues [#1](https://github.com/gabrielavieirab/tarefas-api/issues/1) e
[#9](https://github.com/gabrielavieirab/tarefas-api/issues/9) estão fechadas.

Na consulta de 15/10/2026, o PR #12 não possui review formal registrado.
Seu merge não é tratado como comprovação de aprovação individual de Felipe
ou Caike. Para a etapa 2, **Felipe é o revisor principal** da documentação;
**Gabriela confere clareza e aderência** aos critérios da atividade.

## Dependências e pendências da equipe

- Felipe confere a documentação contra sua auditoria da API e registra erros
  ou correções reais; não são inventados defeitos para preencher o relatório.
- Caike confirma comandos, versões, CI e persistência operacional do volume Docker.
- Gabriela consolida governança, análise crítica de IA e o PDF de submissão.
- A revisão assistida da análise de IA e o relato técnico de Vitor estão
  preparados nos documentos vinculados acima. A análise final ainda depende
  da consolidação de Gabriela e das experiências dos demais integrantes;
  sua homologação humana não é inferida desta preparação.
- A equipe revisa o PDF final e os links antes do envio individual.

Pontos técnicos explicitados nesta atualização: ausência de lock transitivo,
diferença do patch Python local, necessidade de conferir o volume Docker e
metadados incompletos no OpenAPI gerado. Eles não autorizam ampliar o escopo
nem mudar regras sem especificação e testes.

## Checklist da contribuição da etapa 2

- [x] Documentação atualizada para a aplicação integrada.
- [x] README com comandos de instalação, execução e testes.
- [x] Diagramas de arquitetura e fluxo versionados nos documentos.
- [x] ADRs consolidados, com justificativas e limitações.
- [x] Refinamentos e evidências existentes registrados com rastreabilidade.
- [x] Suíte oficial executada: 80 testes aprovados.
- [x] Relato técnico preparado para o relatório consolidado.
- [x] Revisão assistida da análise de IA registrada, com observações e evidências.
- [x] Branch enviada ao GitHub e PR #25 aberto para `develop`, com checks públicos vinculados.
- [ ] Revisão de Felipe e conferência de Gabriela registradas.
- [ ] Ajustes da revisão tratados e contribuição integrada pelo fluxo da equipe.

## Histórico da entrega inicial

Em 05/09/2026, a proposta técnica foi preparada na branch
`feature/especificacao-sdd`, com especificação, quatro ADRs, contrato estático
e 31 critérios de aceitação. A validação do OpenAPI e de seus exemplos naquele
momento era uma verificação do contrato; ainda não havia suíte HTTP na base
consultada. O resultado histórico `no tests ran` não representa o estado atual.
A evolução posterior está em [Refinamentos](refinamentos.md).
