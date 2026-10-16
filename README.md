# API de Gerenciamento de Tarefas

API REST para criação, consulta, atualização e exclusão de tarefas. O projeto foi desenvolvido como parte do Bootcamp utilizando Python, FastAPI, SQLite, SQLAlchemy, Pydantic, pytest, Docker e GitHub Actions.

## Visão geral

A API permite gerenciar tarefas por meio de quatro operações HTTP. Cada tarefa possui um identificador, um título e um status de conclusão.

## Objetivo

Disponibilizar uma API simples e objetiva para registrar tarefas, consultar tarefas existentes, atualizar seus dados ou status de conclusão e removê-las.

## Status do projeto

A API, os testes automatizados, o ambiente Docker e o pipeline de integração contínua estão configurados no repositório.

A suíte automatizada possui 80 testes. Os testes locais e os testes executados dentro do container Docker foram concluídos com sucesso. A persistência do banco SQLite também foi validada utilizando um volume Docker.

## Equipe

| Integrante | Responsabilidade | RA |
|---|---|---|
| Vitor de Assis Patricio Borges | Especificação e decisões técnicas | 22304737 |
| Gabriela Vieira Baptista | GitHub, agente de IA e documentação final | 22510133 |
| Felipe Domingos Ribeiro Pereira | Implementação e banco de dados | 22604250 |
| Caike Ribeiro Menezes | Ambiente, testes e integração contínua | 22601978 |

## Tecnologias

- Python 3.12
- FastAPI
- Uvicorn
- SQLite
- SQLAlchemy
- Pydantic
- pytest
- Docker
- GitHub Actions

## Funcionalidades e rotas

| Método | Rota | Descrição |
|---|---|---|
| `POST` | `/tarefas` | Cria uma nova tarefa. |
| `GET` | `/tarefas` | Lista as tarefas cadastradas. |
| `PATCH` | `/tarefas/{id}` | Atualiza uma tarefa existente ou altera seu status. |
| `DELETE` | `/tarefas/{id}` | Exclui uma tarefa existente. |

Cada tarefa possui os campos `id`, `titulo` e `concluida`.

Exemplo de resposta:

```json
{
  "id": 1,
  "titulo": "Estudar a API",
  "concluida": false
}```

## Pré-requisitos

- Python 3.12
- Git
- Docker Desktop, caso queira executar a API em um container

## Instalação local

Clone o repositório e entre na pasta:

```bash
git clone https://github.com/gabrielavieirab/tarefas-api.git
cd tarefas-api
```

Crie e ative o ambiente virtual no Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Instale as dependências:

```bash
python -m pip install -e ".[test]"
```

Verifique as dependências:

```bash
python -m pip check
```

## Executar os testes

```bash
python -m pytest -v
```

Para gerar um relatório XML:

```powershell
New-Item -ItemType Directory -Force test-results
python -m pytest -v --junitxml=test-results/pytest.xml
```

## Executar a API localmente

```bash
python -m uvicorn app.main:app --reload
```

Documentação interativa: http://127.0.0.1:8000/docs

Listagem de tarefas: http://127.0.0.1:8000/tarefas

## Executar com Docker

Construa a imagem:

```bash
docker build -t tarefas-api .
```

Crie o volume de dados:

```bash
docker volume create tarefas-dados
```

Inicie o container:

```bash
docker run -d --name tarefas-api-container -p 8000:8000 -v tarefas-dados:/data tarefas-api
```

Acesse a documentação: http://localhost:8000/docs

Para executar os testes dentro do container:

```bash
docker exec tarefas-api-container python -m pytest -v
```

O volume `tarefas-dados` preserva os dados do SQLite quando o container é removido e recriado com o mesmo volume.

Para parar e remover o container:

```bash
docker stop tarefas-api-container
docker rm tarefas-api-container
```

## Integração contínua

O GitHub Actions executa o workflow de testes em pushes e pull requests direcionados às branches `main` e `develop`.

O pipeline instala as dependências, verifica o ambiente, executa os testes, constrói a imagem Docker, executa os testes dentro do container e publica os relatórios XML como artefatos.

Consulte as execuções na aba [Actions do GitHub](https://github.com/gabrielavieirab/tarefas-api/actions).

## Evidências de testes

Os resultados detalhados, os critérios de aceitação e as evidências de validação estão documentados em [`docs/evidencias_testes.md`](docs/evidencias_testes.md).