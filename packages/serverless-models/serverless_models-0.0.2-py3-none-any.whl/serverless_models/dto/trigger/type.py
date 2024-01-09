from enum import Enum

from ..base import DtoBase


class TriggerType(int, Enum):
    REST = 1
    TIME = 2
    FUNCTION = 3
    TELEGRAM = 4

    @classmethod
    def to_dict(cls):
        return {item.name: item.value for item in cls}


# API
class TriggerTypeDtoBase(DtoBase):
    type: TriggerType
    can_be_first: bool


# DB
class TriggerTypeInDbDtoBase(TriggerTypeDtoBase):
    id: int


class TriggerTypeInDbDto(TriggerTypeInDbDtoBase):
    pass


# GET
class TriggerTypeDto(TriggerTypeInDbDtoBase):
    pass


# POST
class TriggerTypeCreateDto(TriggerTypeDtoBase):
    pass
