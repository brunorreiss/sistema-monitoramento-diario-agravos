from enum import Enum
from pydantic import BaseModel
from typing import Optional, List, Union


class ResponseSite(BaseModel):
    ANOOBRA: Optional[Union[int, str]]  = ''
    MESOBRA: Optional[Union[int, str]]  = ''
    NUMEROOBRA: Optional[Union[int, str]]  = ''
    OBJETOOBRA: Optional[Union[int, str]]  = ''
    VALOROBRA: Optional[float]  = 0.0
    IDCREDORES: Optional[Union[int, str]]  = ''
    CREDORES: Optional[Union[int, str]]  = ''
    DATAINICIO: Optional[Union[int, str]]  = ''
    DATACONCLUSAO: Optional[Union[int, str]]  = ''
    VALORPARCELASPAGAS: Optional[float]  = 0.0
    IDUNIDADEORCAMENTARIA: Optional[Union[int, str]]  = ''
    CODIGOORGAO: Optional[Union[int, str]]  = ''
    CODIGOUNIDADE: Optional[Union[int, str]]  = ''
    CODIGOCOMPLETOUO: Optional[Union[int, str]]  = ''
    DESCRICAOUO: Optional[Union[int, str]]  = ''

class ResponseDefault(BaseModel):
    code: int
    message: str
    datetime: str
    results: List[ResponseSite]

class ResponseError(BaseModel):
    code: int
    message: str