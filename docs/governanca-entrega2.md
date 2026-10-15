\# Governança da Entrega 2



\## 1. Objetivo



Este documento define as regras de organização, colaboração, revisão e integração utilizadas pela equipe na Entrega 2 do projeto Tarefas API.



A governança tem como objetivos:



\- organizar o trabalho entre os quatro integrantes;

\- evitar alterações diretas na branch principal;

\- garantir revisão entre pares;

\- relacionar Issues, branches, commits e Pull Requests;

\- manter o histórico das decisões;

\- comprovar a participação da equipe;

\- reduzir o risco de integração de código não validado.



\---



\## 2. Identificação do projeto



\- \*\*Projeto:\*\* Tarefas API

\- \*\*Repositório:\*\* https://github.com/gabrielavieirab/tarefas-api

\- \*\*Branch principal:\*\* `main`

\- \*\*Branch de integração:\*\* `develop`

\- \*\*Tecnologias principais:\*\* Python, FastAPI, SQLite, SQLAlchemy, Pydantic, pytest, Docker e GitHub Actions.



\---



\## 3. Integrantes e responsabilidades



| Integrante | RA | Responsabilidade na Entrega 2 |

|---|---:|---|

| Vitor de Assis Patricio Borges | 22304737 | Especificação, arquitetura, README, diagrama e ADRs |

| Gabriela Vieira Baptista | 22510133 | Coordenação, governança, análise crítica de IA e relatório final |

| Felipe Domingos Ribeiro Pereira | 22604250 | Auditoria do código, correções e testes |

| Caike Ribeiro Menezes | 22601978 | CI, Docker, testes integrados e evidências |



As responsabilidades podem ser compartilhadas, mas cada atividade deve possuir um responsável principal e um revisor definido.



\---



\## 4. Fluxo de branches



A equipe utiliza o seguinte fluxo:



```text

main

&#x20; ↓

develop

&#x20; ↓

feature/nome-da-funcionalidade

&#x20; ↓

Pull Request para develop

&#x20; ↓

Code review e GitHub Actions

&#x20; ↓

Merge em develop

&#x20; ↓

Validação final

&#x20; ↓

Pull Request para main

```



\### 4.1 Regras das branches



\- `main` representa a versão estável e publicada.

\- `develop` representa a integração das alterações da Entrega 2.

\- Cada integrante deve trabalhar em uma branch específica.

\- A branch deve ser criada a partir da versão atualizada de `develop`.

\- Não devem ser realizados commits diretamente em `main`.

\- Alterações de código devem utilizar nomes descritivos.

\- A branch deve ser atualizada antes da abertura do Pull Request.



\### 4.2 Exemplos de branches



```text

feature/entrega2-governanca-relatorio

feature/entrega2-auditoria-api

feature/entrega2-testes-evidencias

feature/entrega2-readme-arquitetura

feature/entrega2-analise-ia

```



\---



\## 5. Organização por Issues



Cada atividade da Entrega 2 deve estar associada a uma Issue.



As Issues devem conter:



\- título objetivo;

\- descrição do problema ou atividade;

\- responsável principal;

\- critérios de aceitação;

\- arquivos relacionados;

\- dependências;

\- Pull Request correspondente;

\- situação atual.



\### 5.1 Issues sugeridas



Os números devem ser conferidos no GitHub antes da criação, pois podem ser diferentes dos números sugeridos abaixo.



| Tema | Responsável principal | Apoio |

|---|---|---|

| Governança da Entrega 2 | Gabriela | Toda a equipe |

| Auditoria e refinamento da API | Felipe | Vitor |

| Testes e relatório de erros | Felipe | Caike |

| README, arquitetura e ADRs | Vitor | Felipe |

| CI, Docker e evidências | Caike | Felipe |

| Análise crítica do uso de IA | Gabriela | Vitor |

| Relatório PDF consolidado | Gabriela | Toda a equipe |



\---



\## 6. Critérios de aceitação das Issues



Uma Issue somente deve ser marcada como concluída quando:



\- o trabalho descrito tiver sido realizado;

\- os arquivos alterados estiverem revisados;

\- os testes necessários tiverem sido executados;

\- o Pull Request correspondente tiver sido aberto;

\- outro integrante tiver realizado a revisão;

\- a GitHub Actions estiver aprovada;

\- os comentários da revisão tiverem sido resolvidos;

\- o Pull Request tiver sido integrado;

\- a Issue estiver vinculada ao Pull Request ou ao commit.



Exemplo de critério de aceitação:



> A atividade será considerada concluída quando a alteração estiver em uma branch própria, possuir Pull Request para `develop`, passar pela GitHub Actions, receber revisão de outro integrante e for integrada sem conflitos.



\---



\## 7. Pull Requests



Todo Pull Request deve conter:



\- título claro;

\- descrição do que foi alterado;

\- Issue relacionada;

\- lista de arquivos principais modificados;

\- testes executados;

\- resultado da GitHub Actions;

\- possíveis limitações;

\- revisor indicado.



\### 7.1 Modelo de descrição de Pull Request



```markdown

\## Objetivo



Descrever o objetivo desta alteração.



\## Issue relacionada



Closes #número-da-issue



\## Alterações realizadas



\- Alteração 1

\- Alteração 2

\- Alteração 3



\## Testes executados



```text

python -m pytest -q

Resultado: informar a quantidade de testes aprovados

```



\## Revisão solicitada



Solicito revisão de: nome do integrante.



\## Observações



Informar limitações, decisões ou pontos que precisam de atenção.

```



\---



\## 8. Revisão entre pares



A revisão deve ser feita por outro integrante, preferencialmente de acordo com a seguinte distribuição:



| Tipo de alteração | Responsável | Revisor |

|---|---|---|

| README, arquitetura e ADRs | Vitor | Felipe |

| Análise crítica de IA | Gabriela | Vitor |

| Código e testes | Felipe | Caike |

| CI, Docker e evidências | Caike | Gabriela |



A revisão deve verificar:



\- aderência à especificação;

\- clareza da documentação;

\- qualidade do código;

\- cobertura dos testes;

\- possíveis efeitos colaterais;

\- segurança;

\- consistência com o README e os ADRs;

\- funcionamento da CI;

\- ausência de credenciais ou dados sensíveis.



Nenhum Pull Request deve ser integrado sem revisão e aprovação de outro integrante.



\---



\## 9. Commits



Os commits devem ser pequenos, objetivos e relacionados a uma única finalidade.



Exemplos:



```text

docs: adiciona análise crítica de IA

docs: documenta governança da entrega 2

test: amplia cobertura de validação de tarefas

fix: corrige atualização parcial de tarefa

docs: atualiza README com arquitetura

ci: atualiza evidências da execução

```



Recomenda-se evitar mensagens genéricas como:



```text

ajustes

mudanças

versão final

teste

coisas

```



Antes do commit, o integrante deve revisar:



```powershell

git status

git diff

git diff --check

```



\---



\## 10. GitHub Actions e testes



A GitHub Actions deve ser utilizada para verificar as alterações antes do merge.



A validação deve incluir:



\- instalação das dependências;

\- verificação do ambiente;

\- execução da suíte de testes;

\- construção da imagem Docker;

\- execução dos testes no container;

\- geração dos relatórios de teste.



O resultado da execução deve ser registrado no relatório final com:



\- branch;

\- commit;

\- data;

\- quantidade de testes;

\- resultado;

\- link da execução.



A equipe não deve afirmar que uma validação foi realizada sem uma execução real.



\---



\## 11. Organização do Project



O Project deve utilizar os seguintes status:



| Status | Significado |

|---|---|

| Backlog | Atividade identificada, mas ainda não priorizada |

| A Fazer | Atividade planejada e pronta para começar |

| Em Andamento | Atividade sendo executada |

| Em Revisão | Pull Request aberto aguardando revisão |

| Concluído | Pull Request aprovado, integrado e documentado |



A pessoa responsável pela coordenação deve manter o Project atualizado, principalmente após:



\- criação de uma branch;

\- abertura de um Pull Request;

\- início de uma revisão;

\- aprovação de um Pull Request;

\- integração em `develop`;

\- integração final em `main`.



\---



\## 12. Histórico das sprints



\### Sprint 1 — Preparação e auditoria



Atividades:



\- conferir o estado do repositório;

\- atualizar `develop`;

\- criar as branches da Entrega 2;

\- abrir as Issues;

\- auditar o código e os testes;

\- levantar os requisitos pendentes.



Responsáveis principais:



\- Gabriela: Issues e organização;

\- Felipe: auditoria da API;

\- Caike: validação da CI;

\- Vitor: revisão da especificação.



\### Sprint 2 — Desenvolvimento e documentação



Atividades:



\- corrigir erros encontrados;

\- atualizar os testes;

\- revisar o README;

\- criar o diagrama;

\- consolidar os ADRs;

\- documentar governança e uso de IA.



\### Sprint 3 — Revisão e integração



Atividades:



\- abrir os Pull Requests;

\- realizar revisão entre pares;

\- resolver comentários;

\- executar a GitHub Actions;

\- integrar em `develop`;

\- validar a versão integrada.



\### Sprint 4 — Entrega final



Atividades:



\- integrar a versão final em `main`;

\- atualizar o relatório PDF;

\- conferir os links;

\- revisar a identificação dos integrantes;

\- verificar o repositório público;

\- enviar o arquivo final pela Sala Online.



\---



\## 13. Relação entre Issue, branch, commit e Pull Request



Cada atividade deve manter uma relação rastreável:



```text

Issue

&#x20; ↓

Branch

&#x20; ↓

Commit

&#x20; ↓

Pull Request

&#x20; ↓

Code review

&#x20; ↓

GitHub Actions

&#x20; ↓

Merge

&#x20; ↓

Issue concluída

```



Exemplo:



```text

Issue: Análise crítica do uso de IA

Branch: feature/entrega2-analise-ia

Commit: docs: adiciona analise critica de IA

Pull Request: docs: análise crítica da Entrega 2

Revisor: Vitor

Destino: develop

```



Essa rastreabilidade facilita a comprovação da participação dos integrantes e da evolução do projeto.



\---



\## 14. Responsabilidade da coordenação



A coordenação da Entrega 2 deve:



\- acompanhar o andamento das Issues;

\- verificar se os responsáveis estão definidos;

\- lembrar os integrantes dos prazos;

\- conferir se existem Pull Requests para as atividades;

\- garantir que haja revisão entre pares;

\- verificar o resultado da GitHub Actions;

\- reunir os links das evidências;

\- atualizar o Project;

\- consolidar o relatório final;

\- comunicar pendências ao grupo.



A coordenação não substitui a responsabilidade técnica dos demais integrantes. Cada responsável deve entregar sua parte revisada e documentada.



\---



\## 15. Checklist antes do merge



Antes de aprovar um Pull Request, verificar:



\- \[ ] A alteração está relacionada a uma Issue.

\- \[ ] A branch não é `main`.

\- \[ ] A descrição do Pull Request está preenchida.

\- \[ ] Os testes foram executados.

\- \[ ] A GitHub Actions passou.

\- \[ ] O código foi revisado por outro integrante.

\- \[ ] A documentação foi atualizada, se necessário.

\- \[ ] Não há credenciais ou dados sensíveis.

\- \[ ] Não foram removidos testes para ocultar falhas.

\- \[ ] Os comentários do revisor foram resolvidos.

\- \[ ] Não existem conflitos pendentes.

\- \[ ] O Pull Request pode ser integrado em `develop`.



\---



\## 16. Checklist da entrega final



A Entrega 2 estará pronta quando:



\- \[ ] O repositório estiver público.

\- \[ ] A branch `main` contiver a versão final.

\- \[ ] A branch `develop` tiver sido validada.

\- \[ ] Os quatro integrantes estiverem identificados.

\- \[ ] Os testes automatizados estiverem aprovados.

\- \[ ] A GitHub Actions estiver verde.

\- \[ ] O Docker estiver documentado.

\- \[ ] O README estiver completo.

\- \[ ] O diagrama da arquitetura estiver publicado.

\- \[ ] Os ADRs estiverem revisados.

\- \[ ] Os erros e correções estiverem documentados.

\- \[ ] Os refinamentos da especificação estiverem registrados.

\- \[ ] Os Pull Requests relevantes estiverem vinculados.

\- \[ ] A análise crítica de IA estiver concluída.

\- \[ ] O PDF final estiver revisado pela equipe.

\- \[ ] Os links públicos estiverem funcionando.

\- \[ ] Cada integrante tiver enviado o arquivo solicitado pela Sala Online.



\---



\## 17. Conclusão



A governança da Entrega 2 deve garantir que o projeto não seja avaliado apenas pelo código final, mas também pela forma como foi desenvolvido, revisado e documentado.



O uso de Issues, branches, commits, Pull Requests, code review e GitHub Actions fornece rastreabilidade e reduz o risco de integrar alterações não validadas.



A equipe deve preservar a colaboração entre os integrantes, manter a revisão humana e registrar as decisões relevantes durante todo o ciclo da entrega.



