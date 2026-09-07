"""Cria o arquivo do banco de uso manual e a tabela `tarefas`.

Uso: `python scripts/criar_banco.py` (a partir da raiz do projeto).

Este script fica fora do pacote `app` de propósito: executar um módulo do
pacote diretamente com `python -m app.database` faz o interpretador
carregá-lo duas vezes (uma como `app.database`, outra como `__main__`),
criando duas classes `Base` distintas e deixando `Base.metadata` vazio na
cópia usada por `create_all`. Um script externo evita essa ambiguidade.
"""
from app.database import DATABASE_URL, init_db

if __name__ == "__main__":
    init_db()
    print(f"Banco inicializado em: {DATABASE_URL}")
