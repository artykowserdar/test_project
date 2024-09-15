import enum

from sqlalchemy import (Column, DateTime, Enum, ForeignKey, String, Text)
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship
from sqlalchemy.sql import select

from .database import Base
from .util.sqlalchemy import GUID


# region Enums
class UserRole(enum.Enum):
    system = 'Система'
    admin = 'Администратор'
    user = 'Пользователь'


class UserState(enum.Enum):
    enabled = 'Включен'
    disabled = 'Выключен'
    deleted = 'Удален'


class EntityState(enum.Enum):
    active = 'Активный'
    deleted = 'Удален'


# endregion


# region Action Enums
class UserAction(enum.Enum):
    UserLogIn = 'user.login'
    UserCreate = 'user.create'
    UserEdit = 'user.create'
    UserChangePassword = 'user.pwd-change'
    UserRoleChange = 'user.role-change'
    UserStateChange = 'user.state-change'
    UserLogOut = 'user.logout'
    UserCashRegisterOpen = 'user.cash-register-open'


class NoteAction(enum.Enum):
    NoteAdd = 'payment.add'
    NoteEdit = 'payment.edit'
    NoteStateChange = 'payment.state-change'


# endregion


# region Models
class Users(Base):
    __tablename__ = "tbl_user"
    username = Column(String(256), primary_key=True, index=True)
    fullname = Column(Text(), nullable=False, index=True)
    hashed_password = Column(String(256), nullable=False)
    role = Column(Enum(UserRole), nullable=False)
    state = Column(Enum(UserState), nullable=False)
    create_ts = Column(DateTime(timezone=False), nullable=False)
    update_ts = Column(DateTime(timezone=False), nullable=False)


class UserLog(Base):
    __tablename__ = 'tbl_user_log'
    id = Column(GUID, primary_key=True, index=True)
    username = Column(String(64), ForeignKey(Users.username, deferrable=True), nullable=False)
    action = Column(Enum(UserAction), nullable=False)
    action_user = Column(String(64), ForeignKey(Users.username, deferrable=True), nullable=False)
    sup_info = Column(Text(), nullable=False)
    action_ts = Column(DateTime(timezone=False), nullable=False)


class UserActionLog(Base):
    __tablename__ = 'tbl_user_action_log'
    id = Column(GUID, primary_key=True, index=True)
    username = Column(String(64), ForeignKey(Users.username, deferrable=True), nullable=False, index=True)
    action = Column(Enum(UserAction), nullable=False)
    sup_info = Column(Text(), nullable=True)
    items = Column(Text(), nullable=True)
    action_ts = Column(DateTime(timezone=False), nullable=False)


class Notes(Base):
    __tablename__ = "tbl_note"
    id = Column(GUID, primary_key=True, index=True)
    note_title = Column(String(256), nullable=True, index=True)
    note_text = Column(Text(), nullable=True)
    note_tags = Column(ARRAY(Text), nullable=True, index=True)
    create_user = Column(String(64), ForeignKey(Users.username, deferrable=True), nullable=False)
    state = Column(Enum(EntityState), nullable=False)
    create_ts = Column(DateTime(timezone=False), nullable=False)
    update_ts = Column(DateTime(timezone=False), nullable=False)

    users = relationship("Users", foreign_keys=[create_user])

    @hybrid_property
    def fullname(self):
        if self.users:
            return self.users.fullname
        else:
            return ""

    @fullname.expression
    def fullname(cls):
        return select([Users.fullname]).where(Users.username == cls.create_user).as_scalar()


class NoteLog(Base):
    __tablename__ = 'tbl_note_log'
    id = Column(GUID, primary_key=True, index=True)
    note_id = Column(GUID, ForeignKey(Notes.id, deferrable=True), nullable=False)
    action = Column(Enum(NoteAction), nullable=False)
    action_user = Column(String(64), ForeignKey(Users.username, deferrable=True), nullable=False)
    sup_info = Column(Text(), nullable=False)
    action_ts = Column(DateTime(timezone=False), nullable=False)
# endregion
