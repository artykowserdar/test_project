from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel

from . import config, models


class JWTSettings(BaseModel):
    authjwt_secret_key: str = config.SECRET_KEY


class Token(BaseModel):
    access_token: str
    token_type: str
    role: models.UserRole
    username: str
    fullname: Optional[str]

    class Config:
        orm_mode = True


class TokenData(BaseModel):
    username: Optional[str]

    class Config:
        orm_mode = True


class Users(BaseModel):
    username: Optional[str]
    fullname: Optional[str]
    role: Optional[models.UserRole]
    state: Optional[models.UserState]
    create_ts: Optional[datetime]
    update_ts: Optional[datetime]

    class Config:
        orm_mode = True


class UserInDB(Users):
    hashed_password: str

    class Config:
        orm_mode = True


class UserActionLog(BaseModel):
    id: Optional[UUID]
    username: Optional[str]
    action: Optional[models.UserAction]
    sup_info: Optional[str]
    items: Optional[str]
    action_ts: Optional[datetime]

    class Config:
        orm_mode = True


class Logs(BaseModel):
    id: UUID
    action: Optional[str]
    action_user: Optional[str]
    sup_info: Optional[str]
    action_ts: Optional[datetime]

    class Config:
        orm_mode = True


class Notes(BaseModel):
    id: Optional[UUID]
    note_title: Optional[str]
    note_text: Optional[str]
    create_user: Optional[str]
    state: Optional[models.EntityState]
    create_ts: Optional[datetime]
    update_ts: Optional[datetime]

    class Config:
        orm_mode = True
