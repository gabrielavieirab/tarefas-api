# Roteiro de demonstração — arquitetura e documentação

Material de apoio para a **gravação integral do vídeo por Gabriela**.
Este roteiro cobre o bloco de arquitetura e documentação, com duração estimada
de **45 a 60 segundos**, dentro do vídeo de 3 a 5 minutos da equipe.

## Preparação

Deixar abertos o README, o diagrama em `docs/arquitetura.md` e o Swagger em
`http://127.0.0.1:8000/docs`, com a aplicação em execução. Abrir a versão do
projeto escolhida pela equipe para a gravação. Não é necessário alterar o banco
durante esta etapa; as operações serão apresentadas na demonstração funcional.

A mesma apresentadora conduz a abertura, este bloco técnico, a demonstração
funcional, a execução dos testes e o encerramento. A transição entre os blocos
é feita pela mudança de tela, mantendo a narração contínua.

## Fala sugerida

“A documentação técnica está organizada a partir da especificação As-Built.
No README estão os comandos de instalação, execução e testes, além dos
links para os documentos do projeto.

O diagrama mostra o fluxo: a requisição chega ao FastAPI, passa pela validação
Pydantic, entra na rota e segue para o CRUD. O SQLAlchemy acessa o banco SQLite.
As alterações são confirmadas antes da resposta.

No Swagger estão as quatro operações: criar, listar, atualizar e excluir tarefas.
O PATCH permite editar o título e concluir a tarefa, preservando os campos omitidos,
sem permitir reabertura.

O As-Built registra o que foi implementado, os códigos HTTP, as decisões técnicas
e as limitações conhecidas, mantendo a documentação alinhada ao código.”

## Sequência de tela

Os tempos abaixo são relativos ao início deste bloco técnico.

1. **0 a 12 segundos:** README, comandos e links da documentação.
2. **12 a 30 segundos:** diagrama e caminho FastAPI → validação → CRUD → SQLite.
3. **30 a 45 segundos:** Swagger e as quatro operações, destacando o PATCH.
4. **45 a 60 segundos:** As-Built e links para ADRs/limitações; transição para a demonstração funcional.

Cronometrar no ensaio e ajustar as pausas. Não afirmar equivalência integral entre
Swagger e contrato estático: os validadores ainda têm metadados incompletos no
OpenAPI gerado. Testes, cobertura e Docker são apresentados na etapa de validação do ambiente.
