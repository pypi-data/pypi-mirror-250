from ..base import DtoBase
from .script_way import UserScriptWayCreateDto


# API
class WorkspaceDtoBase(DtoBase):
    pass


# DB
class WorkspaceInDbDtoBase(WorkspaceDtoBase):
    id: int


# GET
class WorkspaceDto(WorkspaceInDbDtoBase):
    id_owner: int


# POST
class WorkspaceCreateDto(WorkspaceDtoBase):
    name_workspace: str
    bindings: list[UserScriptWayCreateDto]
