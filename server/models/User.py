from pydantic import BaseModel
from datetime import date


class TypeServiceModel(BaseModel):
    id: int
    name: str
    description: str | None


class BaseRole(BaseModel):
    name: str
    description: str


class GetRole(BaseRole):
    id: int


class BaseUser(BaseModel):
    name: str
    surname: str
    patronymics: str
    email: str
    phone: str


class GetUser(BaseUser):
    id: int
    trace_id: str
    role: GetRole
    id_role: int
    type_service: TypeServiceModel | None
    id_type_service: int | None


class PostUser(BaseUser):
    password: str
    id_role: int = 0
    id_type_service: int | None
