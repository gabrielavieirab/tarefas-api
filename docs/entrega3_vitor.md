# Contribuição de Vitor — Entrega Final

Responsável: **Vitor de Assis Patricio Borges — RA 22304737 (@vitorborges10)**.
Atualização: **27/10/2026**. Branch: `codex/documentacao-entrega3`, baseada na
`develop` em `668faae`. A implementação conferida já incorpora as auditorias
dos PRs #26/#29, a cobertura de `5c252e7` e a base documental do PR #30 de Gabriela.

## Materiais entregues para revisão

- [Especificação As-Built](especificacao-as-built.md): arquitetura, rotas,
  exemplos, HTTP, modelos, schemas, persistência, ambiente, decisões e limites.
- [SDD atualizada](especificacao_sdd.md): mantém os requisitos e o contrato 1.1.0,
  com o estado da implementação e a ligação ao As-Built.
- [ADRs revisados](decisoes_tecnicas.md): escolhas implementadas, justificativas,
  custos e diferenças da reprodução inicialmente planejada.
- [Diagrama final e fluxo](arquitetura.md#diagrama-final), com
  [fonte Mermaid](diagramas/arquitetura-final.mmd) reutilizável no relatório.
- [README revisado](../README.md): estado atual, arquitetura, instalação,
  execução, testes/cobertura, Docker e caminhos da documentação.
- [Evidências](evidencias_testes.md#entrega-final--27102026) e
  [refinamentos](refinamentos.md): resultados e diferenças rastreáveis.
- [Roteiro do vídeo](roteiro-video-vitor.md): fala e sequência de demonstração.

O arquivo `entrega_vitor.md` preserva o histórico da entrega 2. O As-Built iniciado
por Gabriela é completado no mesmo caminho, evitando duas especificações finais
concorrentes. A retrospectiva e o PDF consolidado permanecem sob coordenação dela.

## Resultado da conferência

Suíte oficial executada: **81 aprovados, zero falhas e um aviso de descontinuação**.
Cobertura local de `app/`: **91% de linhas** (135 de 148 instruções), com Python
3.12.6. `pip check` não encontrou dependências quebradas. A
[CI da base](https://github.com/gabrielavieirab/tarefas-api/actions/runs/40586231416),
com Python 3.12.10, concluiu testes no runner, build e testes Docker com sucesso.
Os resultados locais e remotos são evidências distintas.

A documentação foi conferida com os módulos de `app/`, o Dockerfile, o workflow,
`pyproject.toml`, os testes e o OpenAPI gerado. A conferência OpenAPI adicional
não integra a contagem da suíte. Código, testes e infraestrutura não são alterados
por esta contribuição.

## Parecer técnico para a consolidação de Gabriela

O material técnico desta contribuição descreve quatro operações HTTP e uma única
tabela, preservando o contrato 1.1.0. Estão explícitos o título normalizado de 1 a
120 caracteres, o PATCH parcial sem reabertura, a distinção entre 404 e 422 e o
DELETE sem corpo. O fluxo e os schemas correspondem à base `668faae` conferida.

O relatório final pode usar os resultados acima, identificando a base, o ambiente
e a origem da cobertura. Deve também registrar os limites: metadados incompletos
dos validadores no OpenAPI gerado; ausência de lock transitivo, pin de pytest-cov
e digest da imagem; caminhos sem cobertura medida; e volume Docker sem evidência
operacional local nesta conferência.

O contrato da API é 1.1.0, o pacote é 0.1.0 e a Release prevista é v1.0.0. O PDF
deve nomear cada identificador corretamente e usar links reais para a Release,
o vídeo e os resultados. Não apresentar 81 testes aprovados como 100% de cobertura.

**Situação do PDF:** a versão final da Entrega 3 não foi fornecida nesta etapa.
Este é o parecer sobre os documentos técnicos revisados, não uma aprovação de
um PDF não inspecionado. Quando Gabriela disponibilizá-lo, conferir a transcrição
destes dados, as figuras e os links antes de registrar a revisão técnica final.

## Checklist da contribuição

- [x] Base atual de `develop` conferida, após auditoria e atualização da cobertura.
- [x] SDD e As-Built alinhados com a implementação.
- [x] Arquitetura, fluxo, rotas, HTTP, modelo e schemas descritos.
- [x] ADRs revisados e diferenças do planejamento registradas.
- [x] Diagrama final e README preparados.
- [x] Testes e cobertura executados; origem e limites registrados.
- [x] Parecer técnico dos documentos preparado para a consolidação.
- [x] Roteiro da participação de Vitor no vídeo preparado.
- [ ] Revisão dos colegas registrada no PR e contribuição integrada em `develop`.
- [ ] PDF final de Gabriela recebido e revisado tecnicamente.
- [ ] Participação no vídeo gravada e conferida pela equipe.

Release, publicação do vídeo e submissão do PDF são coordenadas por Gabriela.
