"""Modelo ORM da tabela `tarefas` (seção 6 de docs/especificacao_sdd.md)."""
from sqlalchemy import Boolean, Column, Integer, String

from app.database import Base


class Tarefa(Base):
    """Uma tarefa da lista compartilhada (não há conceito de usuário).

    - id: inteiro positivo gerado pelo banco (rowid do SQLite), chave
      primária e não nulo. O SQLite usa um inteiro assinado de 64 bits
      para o rowid, cobrindo o limite de 9223372036854775807 exigido
      pela especificação sem necessidade de um tipo adicional. Não há
      exigência de numeração sem lacunas nem de o primeiro ID ser 1.
    - titulo: texto obrigatório e não nulo. O limite de 1 a 120 caracteres
      após normalização (RN-03) é responsabilidade da camada de validação
      da aplicação (Pydantic, ainda não implementada nesta contribuição);
      declarar `String(120)` aqui não substitui essa validação.
    - concluida: booleano não nulo, iniciando em `False` (RN-01). O
      SQLAlchemy mapeia para `0`/`1` no SQLite, como previsto na ADR-002.
    """

    __tablename__ = "tarefas"

    id = Column(Integer, primary_key=True, autoincrement=True)
    titulo = Column(String(120), nullable=False)
    concluida = Column(Boolean, nullable=False, default=False, server_default="0")

    def __repr__(self) -> str:  # pragma: no cover - apoio a depuração
        return f"Tarefa(id={self.id!r}, titulo={self.titulo!r}, concluida={self.concluida!r})"
