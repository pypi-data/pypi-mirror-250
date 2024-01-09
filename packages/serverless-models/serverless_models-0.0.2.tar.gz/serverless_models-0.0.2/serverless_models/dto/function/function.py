from datetime import datetime

from ..base import DtoBase
from ..user import UserInDbDto
from .tag import FunctionTagInDbDto


# API
class FunctionDtoBase(DtoBase):
    datetime_creation: datetime
    description: str
    file: str
    name: str
    is_public: bool


# DB
class FunctionInDbDtoBase(FunctionDtoBase):
    id: int


class FunctionInDbDto(FunctionInDbDtoBase):
    owner: UserInDbDto
    tags: list[FunctionTagInDbDto]


# GET
class FunctionDto(FunctionInDbDtoBase):
    pass


# POST
class FunctionCreateDto(FunctionDtoBase):
    id_owner: int
