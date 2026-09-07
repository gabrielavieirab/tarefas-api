"""Esquemas Pydantic de entrada/saída (seção 7 e 8 de docs/especificacao_sdd.md
e docs/openapi.json). Implementam a ADR-003 (contratos pequenos e explícitos):
POST aceita só `titulo`; PATCH aceita `titulo`, `concluida: true` ou ambos,
exigindo pelo menos um; campos extras e `null` explícito são rejeitados.
"""
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


def _validar_titulo(valor: Any) -> str:
    """Normaliza e valida um título conforme RN-02/RN-03.

    - Deve ser uma string JSON (rejeita null, número, booleano, lista, objeto).
    - Remove espaços em branco das extremidades antes de medir o tamanho.
    - 1 a 120 caracteres Unicode após a normalização; mantém acentos,
      maiúsculas/minúsculas e espaços internos.
    """
    if not isinstance(valor, str):
        raise ValueError("titulo deve ser uma string.")
    texto = valor.strip()
    if not (1 <= len(texto) <= 120):
        raise ValueError(
            "titulo deve ter de 1 a 120 caracteres após remover espaços das extremidades."
        )
    return texto


class TarefaCreate(BaseModel):
    """Corpo de POST /tarefas. Só aceita `titulo` (RN-04)."""

    model_config = ConfigDict(extra="forbid")

    titulo: str

    @field_validator("titulo", mode="before")
    @classmethod
    def _valida_titulo(cls, v: Any) -> str:
        return _validar_titulo(v)


class TarefaAtualizar(BaseModel):
    """Corpo de PATCH /tarefas/{id} (RN-05).

    `titulo` e `concluida` são opcionais, mas ao menos um deve ser enviado;
    campo omitido preserva o valor atual, enquanto `null` explícito é
    inválido — por isso a validação usa `model_fields_set` em vez de tratar
    `None` como "não informado".
    """

    model_config = ConfigDict(extra="forbid")

    titulo: str | None = None
    concluida: bool | None = None

    @field_validator("titulo", mode="before")
    @classmethod
    def _valida_titulo(cls, v: Any) -> str:
        if v is None:
            raise ValueError("titulo não pode ser null.")
        return _validar_titulo(v)

    @field_validator("concluida", mode="before")
    @classmethod
    def _valida_concluida(cls, v: Any) -> bool:
        # `is not True` (em vez de `!= True`) rejeita 1, "true" etc., que são
        # iguais a True por igualdade mas não pelo tipo (RN-05).
        if v is not True:
            raise ValueError("concluida só aceita o valor booleano true.")
        return v

    @model_validator(mode="after")
    def _ao_menos_um_campo(self) -> "TarefaAtualizar":
        if not self.model_fields_set:
            raise ValueError("Envie ao menos um dos campos: titulo, concluida.")
        return self


class TarefaRead(BaseModel):
    """Representação de saída de uma tarefa (seção 8 da especificação)."""

    model_config = ConfigDict(from_attributes=True, extra="forbid")

    id: int
    titulo: str
    concluida: bool


class TarefaNaoEncontrada(BaseModel):
    """Corpo do erro 404 (RF-06), com a mensagem fixa do contrato."""

    model_config = ConfigDict(extra="forbid")

    detail: str = "Tarefa não encontrada."
