\# Especificação Técnica As-Built



\## 1. Identificação do projeto



Nome: Tarefas API



Repositório:

https://github.com/gabrielavieirab/tarefas-api



A aplicação é uma API REST para gerenciamento de tarefas. Ela permite criar, consultar, atualizar, concluir e excluir tarefas por meio de requisições HTTP.



\## 2. Objetivo da aplicação



O sistema foi desenvolvido para representar o ciclo de vida de tarefas de forma simples, documentada e testável.



A API permite que uma aplicação cliente gerencie tarefas persistidas em banco de dados, com validação dos dados recebidos e respostas HTTP padronizadas.



\## 3. Arquitetura final



A aplicação foi desenvolvida em Python utilizando o framework FastAPI.



O fluxo de uma requisição é:



Cliente HTTP → rota FastAPI → validação Pydantic/FastAPI → camada CRUD → sessão SQLAlchemy → banco SQLite → resposta HTTP.



A organização do projeto separa as responsabilidades entre rotas, schemas, persistência, modelos, banco de dados e testes automatizados.



\## 4. Tecnologias utilizadas



\- Python;

\- FastAPI;

\- Uvicorn;

\- SQLite;

\- SQLAlchemy;

\- Pydantic;

\- pytest;

\- HTTPX;

\- Docker;

\- GitHub Actions;

\- Git e GitHub.



\## 5. Estrutura principal do projeto



\- `app/main.py`: criação e configuração da aplicação;

\- `app/routes.py`: definição das rotas HTTP;

\- `app/schemas.py`: schemas e validação dos dados;

\- `app/crud.py`: operações de criação, consulta, atualização e exclusão;

\- `app/models.py`: modelo da tabela de tarefas;

\- `app/database.py`: configuração do banco SQLite e das sessões;

\- `tests/`: testes automatizados;

\- `docs/`: documentação técnica do projeto;

\- `Dockerfile`: configuração do ambiente Docker;

\- `.github/workflows/tests.yml`: configuração da integração contínua;

\- `pyproject.toml`: dependências e configuração do projeto;

\- `README.md`: instruções de instalação e execução.



\## 6. API entregue



\### 6.1 POST /tarefas



Cria uma nova tarefa.



A requisição recebe um título válido. A tarefa é criada com um identificador gerado pelo banco e começa com o campo `concluida` definido como `false`.



Resposta de sucesso: `201 Created`.



\### 6.2 GET /tarefas



Retorna a lista de tarefas cadastradas no banco de dados.



Resposta de sucesso: `200 OK`.



\### 6.3 PATCH /tarefas/{id}



Atualiza parcialmente uma tarefa existente.



A rota permite alterar o título, o estado de conclusão ou os dois campos ao mesmo tempo. Os campos não enviados são preservados.



Resposta de sucesso: `200 OK`.



Para uma tarefa inexistente, a API retorna `404 Not Found`.



\### 6.4 DELETE /tarefas/{id}



Exclui uma tarefa existente.



Resposta de sucesso: `204 No Content`, sem corpo de resposta.



Para uma tarefa inexistente, a API retorna `404 Not Found`.



\## 7. Validações e códigos HTTP



A API rejeita:



\- títulos ausentes;

\- títulos vazios;

\- títulos inválidos;

\- títulos acima do limite definido;

\- campos extras não previstos;

\- corpos vazios no PATCH;

\- identificadores inexistentes.



Os principais códigos HTTP utilizados são:



\- `200 OK`: consulta ou atualização realizada com sucesso;

\- `201 Created`: tarefa criada com sucesso;

\- `204 No Content`: tarefa excluída com sucesso;

\- `404 Not Found`: tarefa não encontrada;

\- `422 Unprocessable Entity`: dados de entrada inválidos.



\## 8. Persistência



A aplicação utiliza SQLite para persistência dos dados e SQLAlchemy para o mapeamento e acesso ao banco.



As tarefas são armazenadas no banco e permanecem disponíveis entre reinicializações, conforme o ambiente de execução.



Os testes utilizam banco temporário e isolamento próprio para evitar alterações no banco utilizado manualmente pela aplicação.



\## 9. Testes homologados



A suíte de testes verifica:



\- criação de tarefas;

\- listagem de tarefas;

\- atualização de títulos;

\- conclusão de tarefas;

\- preservação dos campos omitidos no PATCH;

\- exclusão de tarefas;

\- títulos ausentes, vazios ou inválidos;

\- limite de caracteres;

\- rejeição de campos extras;

\- corpo vazio no PATCH;

\- identificadores inexistentes;

\- respostas 404 e 422;

\- persistência no SQLite;

\- isolamento do banco nos testes;

\- códigos de resposta HTTP;

\- documentação das respostas da API.



A quantidade final de testes e o percentual de cobertura serão registrados após a execução final da suíte de homologação.



\## 10. Execução local



Para instalar as dependências de desenvolvimento:



```bash

python -m pip install -e ".\[test]"



