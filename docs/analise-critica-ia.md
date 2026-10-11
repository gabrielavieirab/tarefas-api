\# Análise crítica do uso de Inteligência Artificial



\## 1. Objetivo



Este documento apresenta uma análise crítica sobre o uso de ferramentas de Inteligência Artificial durante o desenvolvimento da API de gerenciamento de tarefas.



A análise considera os benefícios, limitações, riscos éticos e riscos técnicos associados ao uso de agentes de IA no ciclo de vida de software, especialmente nas etapas de especificação, implementação, testes, documentação e revisão.



A Inteligência Artificial foi considerada uma ferramenta de apoio à equipe. As decisões finais, a validação do código e a responsabilidade pela entrega permaneceram sob responsabilidade dos integrantes do grupo.



\---



\## 2. Ferramentas utilizadas ou avaliadas



A equipe deve preencher esta tabela somente com ferramentas que realmente foram utilizadas ou avaliadas durante o projeto.



| Ferramenta | Utilizada ou avaliada? | Finalidade | Integrante que utilizou |

|---|---|---|---|

| Claude Code | \[Sim/Não] | \[Descrever a finalidade] | \[Nome] |

| Codex CLI | \[Sim/Não] | \[Descrever a finalidade] | \[Nome] |

| Cursor | \[Sim/Não] | \[Descrever a finalidade] | \[Nome] |

| Antigravity | \[Sim/Não] | \[Descrever a finalidade] | \[Nome] |

| Outra ferramenta | \[Sim/Não] | \[Informar qual e a finalidade] | \[Nome] |



As ferramentas não utilizadas não devem ser apresentadas como responsáveis por partes do projeto. Quando uma ferramenta foi apenas pesquisada ou comparada, essa diferença deve ser registrada claramente.



\---



\## 3. Matriz comparativa



A comparação deve considerar somente as ferramentas efetivamente utilizadas ou avaliadas pela equipe.



| Critério | \[Ferramenta 1] | \[Ferramenta 2] | \[Ferramenta 3] |

|---|---|---|---|

| Facilidade de uso | \[Avaliação] | \[Avaliação] | \[Avaliação] |

| Compreensão do contexto | \[Avaliação] | \[Avaliação] | \[Avaliação] |

| Apoio à especificação | \[Avaliação] | \[Avaliação] | \[Avaliação] |

| Geração de código | \[Avaliação] | \[Avaliação] | \[Avaliação] |

| Geração de testes | \[Avaliação] | \[Avaliação] | \[Avaliação] |

| Apoio à documentação | \[Avaliação] | \[Avaliação] | \[Avaliação] |

| Risco de erros | \[Avaliação] | \[Avaliação] | \[Avaliação] |

| Necessidade de revisão humana | \[Avaliação] | \[Avaliação] | \[Avaliação] |

| Impacto no projeto | \[Avaliação] | \[Avaliação] | \[Avaliação] |



\### 3.1 Avaliação das ferramentas



A avaliação deve ser baseada na experiência real da equipe. É importante registrar situações concretas em que a ferramenta ajudou, apresentou uma limitação ou exigiu correção humana.



\#### \[Nome da ferramenta]



\*\*Pontos positivos:\*\*



\- \[Descrever o benefício observado.]

\- \[Descrever outro benefício observado.]

\- \[Informar se ajudou na documentação, testes, código ou especificação.]



\*\*Limitações observadas:\*\*



\- \[Descrever uma limitação real.]

\- \[Informar se a ferramenta gerou respostas incompletas ou imprecisas.]

\- \[Informar se foi necessário fornecer contexto adicional.]



\*\*Impacto no projeto:\*\*



\[Descrever se a ferramenta ajudou a economizar tempo, melhorar a documentação, identificar casos de teste ou organizar o trabalho.]



\*\*Necessidade de revisão humana:\*\*



\[A ferramenta não deve ser considerada autoridade. Toda sugestão foi revisada, adaptada e validada pela equipe antes de ser aceita.]



Repita esta seção para cada ferramenta utilizada ou avaliada.



\---



\## 4. Benefícios observados no uso de IA



O uso de Inteligência Artificial pode contribuir para diversas atividades do desenvolvimento de software, desde que seja supervisionado por pessoas.



No projeto Tarefas API, a IA pode apoiar ou apoiar em situações como:



\- organização inicial das tarefas;

\- elaboração de sugestões para documentação;

\- identificação de cenários de teste;

\- revisão de textos técnicos;

\- explicação de erros de programação;

\- sugestão de estruturas para README e ADRs;

\- comparação de alternativas técnicas;

\- identificação de casos de borda;

\- apoio na preparação de exemplos de requisições e respostas.



Esses benefícios não eliminam a necessidade de conhecimento técnico. A equipe precisa compreender o problema, avaliar as sugestões e decidir quais alterações realmente fazem sentido para o projeto.



\---



\## 5. Riscos de alucinação de código



Agentes de IA podem produzir respostas que parecem corretas, mas que contêm informações inventadas ou incompatíveis com o projeto. Esse problema é conhecido como alucinação.



Entre os riscos estão:



\- inventar bibliotecas, funções ou parâmetros;

\- sugerir endpoints que não existem na especificação;

\- utilizar versões incompatíveis das dependências;

\- afirmar que um teste foi executado sem que ele tenha sido executado;

\- interpretar incorretamente os requisitos;

\- criar código que funciona apenas em um caso simples;

\- ignorar cenários de borda;

\- sugerir mudanças incompatíveis com o banco de dados;

\- alterar o comportamento de uma rota sem atualizar os testes e a documentação.



No projeto Tarefas API, uma sugestão incorreta poderia afetar, por exemplo:



\- o comportamento do `PATCH`;

\- a diferença entre respostas `404` e `422`;

\- a validação de títulos;

\- a persistência dos dados no SQLite;

\- a geração dos identificadores;

\- a resposta `204` do endpoint `DELETE`.



Por esse motivo, nenhuma sugestão de IA deve ser aceita apenas porque o código parece plausível.



\---



\## 6. Riscos de código inseguro ou destrutivo



Uma ferramenta de IA pode sugerir comandos ou alterações que causam danos ao ambiente ou ao repositório.



Exemplos de riscos:



\- apagar arquivos ou diretórios;

\- remover testes para fazer a suíte passar;

\- sobrescrever configurações importantes;

\- apagar dados do banco SQLite;

\- modificar a branch errada;

\- executar comandos destrutivos sem confirmação;

\- inserir dependências desnecessárias;

\- desabilitar validações;

\- expor informações sensíveis em logs;

\- criar configurações inseguras para produção.



Para reduzir esses riscos, a equipe deve:



1\. ler os comandos antes de executá-los;

2\. verificar a branch atual;

3\. manter cópias ou utilizar o Git para recuperar alterações;

4\. revisar o diff antes do commit;

5\. não executar comandos destrutivos sem entender seus efeitos;

6\. preservar os testes existentes;

7\. executar a suíte automatizada após as alterações;

8\. solicitar revisão de outro integrante.



\---



\## 7. Privacidade, vazamento de dados e confidencialidade



Não devem ser enviados para ferramentas de IA:



\- senhas;

\- tokens de autenticação;

\- chaves de API;

\- credenciais do GitHub;

\- dados pessoais desnecessários;

\- informações privadas dos integrantes;

\- arquivos confidenciais;

\- dados de usuários reais;

\- informações internas que não sejam necessárias para a tarefa.



Antes de enviar um arquivo ou trecho de código para uma ferramenta de IA, a equipe deve verificar se ele contém informações sensíveis.



Quando possível, devem ser utilizados:



\- dados fictícios;

\- exemplos anonimizados;

\- variáveis de ambiente sem seus valores reais;

\- trechos mínimos necessários para a análise;

\- cópias sem credenciais ou tokens.



A responsabilidade pela proteção das informações continua sendo da equipe, mesmo quando a sugestão é produzida por uma ferramenta automatizada.



\---



\## 8. Propriedade intelectual e direitos autorais



O código produzido com auxílio de IA deve ser tratado com responsabilidade. A utilização de uma sugestão gerada por IA não elimina a necessidade de verificar:



\- licenças das bibliotecas utilizadas;

\- compatibilidade entre dependências;

\- possível reprodução de trechos de código de terceiros;

\- regras da instituição de ensino;

\- direitos autorais de imagens, textos e exemplos;

\- origem de soluções copiadas ou adaptadas.



A equipe deve compreender e revisar o código que utiliza. O fato de uma ferramenta gerar determinado trecho não significa automaticamente que ele esteja livre de restrições ou adequado ao projeto.



Também é importante registrar, de forma transparente, quando a IA foi utilizada como apoio relevante na especificação, no código, nos testes ou na documentação.



\---



\## 9. Centralidade da revisão humana



A revisão humana é obrigatória em todas as alterações relevantes. A IA pode sugerir, explicar ou acelerar tarefas, mas não deve substituir a decisão dos integrantes.



Antes de integrar uma alteração sugerida por IA, a equipe deve:



1\. comparar a sugestão com a especificação do projeto;

2\. verificar se a alteração respeita o escopo;

3\. revisar o código manualmente;

4\. executar os testes automatizados;

5\. avaliar cenários normais e de borda;

6\. verificar segurança e privacidade;

7\. atualizar a documentação, se necessário;

8\. solicitar revisão de outro integrante no Pull Request.



O fluxo adotado deve ser:



```text

Sugestão da IA

&#x20;       ↓

Análise do integrante

&#x20;       ↓

Implementação ou adaptação

&#x20;       ↓

Testes automatizados

&#x20;       ↓

Code review

&#x20;       ↓

Aprovação humana

&#x20;       ↓

Merge

```



Nenhuma resposta de IA deve ser utilizada como prova de que o sistema funciona. A comprovação deve ser feita por meio de execução real, testes, revisão e evidências.



\---



\## 10. Uso da IA no fluxo SDD



O desenvolvimento orientado por especificação exige que o comportamento esperado seja definido antes da implementação.



Nesse fluxo, a IA pode ajudar a:



\- organizar requisitos;

\- sugerir critérios de aceitação;

\- identificar ambiguidades;

\- propor casos de teste;

\- explicar alternativas técnicas;

\- revisar a clareza de uma especificação.



Entretanto, a especificação deve ser aprovada pela equipe. A IA não deve alterar automaticamente regras de negócio apenas para fazer um teste passar.



Quando um teste revelar um problema, a equipe deve primeiro verificar se:



\- o código está incorreto;

\- o teste está incorreto;

\- a especificação está ambígua;

\- o requisito precisa ser refinado.



Qualquer mudança de comportamento deve ser documentada e revisada antes de ser implementada.



\---



\## 11. Conclusão



A Inteligência Artificial pode aumentar a produtividade e apoiar a equipe em tarefas de planejamento, implementação, testes e documentação. Porém, seu uso envolve riscos técnicos, éticos e de segurança.



No projeto Tarefas API, a IA deve ser tratada como uma ferramenta auxiliar, e não como substituta da equipe. A responsabilidade pelas decisões, pelo código integrado e pela qualidade da entrega permanece com os integrantes.



A qualidade final depende da combinação entre:



\- especificação clara;

\- conhecimento técnico;

\- revisão humana;

\- testes automatizados;

\- code review;

\- governança de branches e Pull Requests;

\- cuidado com segurança, privacidade e propriedade intelectual.





