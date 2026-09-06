# Minha contribuição - entrega inicial

Nesta contribuição, preparei a especificação e as decisões técnicas da
[Issue #1](https://github.com/gabrielavieirab/tarefas-api/issues/1), na branch
`feature/especificacao-sdd`, para integração em `develop` por PR.

## Materiais que preparei

- `especificacao_sdd.md`: problema, escopo, requisitos funcionais e não funcionais,
  modelo, regras e exemplos das quatro operações.
- `decisoes_tecnicas.md`: escolha e justificativa das tecnologias, quatro ADRs,
  arquitetura, componentes e interfaces para desenvolvimento e testes.
- `openapi.json`: contrato HTTP 3.1.0, com entradas, saídas, erros e exemplos.
- `criterios_aceitacao.md`: cenários rastreáveis para Felipe e Caike.
- `refinamentos.md`: origem das decisões iniciais e registro de feedback futuro.
- `../README.md`: resumo técnico e links para a documentação, como contribuição
  à consolidação final de Gabriela.

Todos os documentos descrevem a proposta técnica, sujeita à revisão dos colegas.
O OpenAPI é um contrato estático elaborado antes da implementação; depois, a
documentação gerada pelo FastAPI deve ser conferida contra ele. No cadastro e na
edição, o contrato permite espaços nas extremidades do título e limita o conteúdo
após normalização; essa transformação precisa ser refletida na validação da aplicação.

Na versão 1.1.0, incluí a edição do texto da tarefa no PATCH, com preservação de ID
e campos omitidos. Mantive quatro operações HTTP e acrescentei cinco cenários,
totalizando 31 critérios de aceitação.

## Como as responsabilidades se conectam

**Gabriela** usa a especificação e os ADRs para alinhar as instruções da IA e
consolidar README/PDF. Ela mantém a organização do repositório e a documentação
do uso real da ferramenta. A seção adicionada ao README dá acesso à parte técnica;
os comandos e as evidências serão complementados nas tarefas correspondentes.

**Felipe** implementa os componentes e as quatro rotas com base nos contratos.
Deve revisar principalmente edição parcial no PATCH, normalização do título,
persistência, campos extras e os códigos HTTP antes da implementação.

**Caike** prepara dependências, container, testes e CI. Usa os critérios de aceitação
e valida o isolamento do banco. A escolha de Python 3.12 e o comando de instalação
de `AGENTS.md` orientam sua configuração; as versões exatas ficam registradas
quando ele validar o conjunto integrado.

**Minha responsabilidade:** manterei contratos e decisões coerentes, esclarecerei
dúvidas e registrarei mudanças motivadas por revisão ou testes. A implementação, os testes, o Dockerfile,
o workflow e o PDF de submissão permanecem nas tarefas dos responsáveis definidos.

## Validação desta contribuição

Em 05/09/2026, validei o contrato com `openapi-spec-validator` 0.9.0:

```text
python -m openapi_spec_validator docs/openapi.json
docs/openapi.json: OK
```

Na versão 1.1.0, conferi 75 exemplos válidos e inválidos dos esquemas de cadastro
e atualização, incluindo edição isolada, conclusão isolada, edição e conclusão
juntas, campos omitidos, `null`, limites do título e campos extras. Conferi também
os 12 exemplos embutidos no OpenAPI, a ausência de conteúdo no `204`, as quatro
operações e os 12 links internos dos documentos.
São verificações do contrato estático, não testes HTTP de uma aplicação implementada.
Instalei as ferramentas de validação em ambiente temporário separado,
sem definir as dependências da aplicação que Caike vai preparar.

Também executei `pytest --ignore=tmp --ignore=output -p no:cacheprovider`,
conforme a instrução de executar pytest antes do PR. Resultado: `collected 0 items`
e `no tests ran`. Não existe suíte da API na base consultada; esse resultado
não comprova aprovação de testes nem conclusão do harness da entrega.

## Conclusão da minha parte

- [x] Descrevi o problema, o escopo e os requisitos.
- [x] Defini os campos, as regras, as entradas, as saídas e os códigos HTTP.
- [x] Justifiquei as tecnologias e separei os componentes.
- [x] Preparei os critérios de aceitação e o registro de refinamentos.
- [ ] PR revisado por Felipe e Caike, como exige a Issue #1.
- [ ] Tratarei e registrarei o feedback real da revisão.
- [ ] PR aprovado e integrado em `develop` pelo fluxo do grupo.

Depois da integração das outras contribuições, também participarei da
[Issue #9](https://github.com/gabrielavieirab/tarefas-api/issues/9), conferindo rotas,
testes e especificação. Essa revisão futura depende de código e evidências que
ainda serão produzidos; não está marcada como concluída nesta documentação.

## Roteiro de revisão para os colegas

1. Ler a seção de regras e os contratos em `especificacao_sdd.md`.
2. Conferir as escolhas e a decomposição em `decisoes_tecnicas.md`.
3. Verificar os casos de borda em `criterios_aceitacao.md`.
4. Comentar no PR qualquer dificuldade concreta ou regra ambígua.
5. Ajustarei os documentos afetados e registrarei o feedback.
6. Aprovar o PR quando os pontos estiverem resolvidos; não fazer merge sem revisão.
