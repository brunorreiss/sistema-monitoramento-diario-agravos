from enum import Enum
from pydantic import BaseModel
from typing import List


class Doenca(BaseModel):
    nome_doenca: str
    positivo: str
    negativo: str
    silenciado: str


class ResponseSite(BaseModel):
    nome_hospital: str
    doencas: List[Doenca]


class ResponseDefault(BaseModel):
    code: int
    message: str
    datetime: str
    results: List[ResponseSite]


class ResponseError(BaseModel):
    code: int
    message: str
