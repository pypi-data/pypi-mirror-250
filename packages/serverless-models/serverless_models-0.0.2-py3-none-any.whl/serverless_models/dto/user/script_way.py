from serverless_models.dto.trigger.trigger import TriggerDtoBase

from ..base import DtoBase  # type: ignore


# API
class UserScriptWayDtoBase(DtoBase):
    trigger: TriggerDtoBase
    id_function: int
    name_unique: str


# DB
class UserScriptWayInDbDtoBase(UserScriptWayDtoBase):
    id: int


class UserScriptWayInDtoDb(UserScriptWayInDbDtoBase):
    pass


# POST
class UserScriptWayCreateDto(UserScriptWayDtoBase):
    pass


class UserScriptWayUpdateDto(UserScriptWayDtoBase):
    pass


# GET
class UserScriptWayDto(UserScriptWayInDbDtoBase):
    workspace_id: int
