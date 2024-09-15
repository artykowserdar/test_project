import logging

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import FlushError

from app import models
from app.accesses import token_access
from app.cruds import user_crud

log = logging.getLogger(__name__)


# region Users
def get_user(db: Session, username: str):
    db_user = user_crud.get_active_user_by_username(db, username)
    if db_user is None:
        return None
    return db_user


def add_user(db: Session, username, password, role, fullname, action_user):
    try:
        status = 200
        error_msg = ''
        hash_password = token_access.get_password_hash(password)
        db_user = user_crud.add_user(db, username, hash_password, role, fullname, action_user)
        if db_user is None:
            status = 418
            error_msg = 'add_user_failed'
    except (IntegrityError, FlushError) as exc:
        log.exception('%s - %s', exc, action_user)
        db.rollback()
        status = 418
        db_user = None
        error_msg = 'add_user_error'
    return {"status": status, "error_msg": error_msg, "result": db_user}


def edit_user(db: Session, username, role, fullname, action_user):
    try:
        status = 200
        error_msg = ''
        db_user = user_crud.edit_user(db, username, role, fullname, action_user)
        if db_user is None:
            status = 418
            error_msg = 'edit_user_failed'
    except (IntegrityError, FlushError) as exc:
        log.exception('%s - %s', exc, action_user)
        db.rollback()
        status = 418
        db_user = None
        error_msg = 'edit_user_error'
    return {"status": status, "error_msg": error_msg, "result": db_user}


def change_user_password(db: Session, username, password, action_user):
    try:
        user = get_user_by_username(db, username)
        status = user["status"]
        error_msg = user["error_msg"]
        if status == 418:
            return {"status": status, "error_msg": error_msg, "result": user["result"]}
        hash_password = token_access.get_password_hash(password)
        db_user = user_crud.change_user_password(db, username, hash_password, action_user)
        if db_user is None:
            status = 418
            error_msg = 'change_user_password_failed'
    except (IntegrityError, FlushError) as exc:
        log.exception('%s - %s', exc, action_user)
        db.rollback()
        status = 418
        db_user = None
        error_msg = 'change_user_password_error'
    return {"status": status, "error_msg": error_msg, "result": db_user}


def change_user_role(db: Session, username, role, action_user):
    try:
        user = get_user_by_username(db, username)
        status = user["status"]
        error_msg = user["error_msg"]
        if status == 418:
            return {"status": status, "error_msg": error_msg, "result": user["result"]}
        db_user = user_crud.change_user_role(db, username, role, action_user)
        if db_user is None:
            status = 418
            error_msg = 'change_user_role_failed'
    except (IntegrityError, FlushError) as exc:
        log.exception('%s - %s', exc, action_user)
        db.rollback()
        status = 418
        db_user = None
        error_msg = 'change_user_role_error'
    return {"status": status, "error_msg": error_msg, "result": db_user}


def change_user_state(db: Session, username, state, action_user):
    try:
        user = get_user_by_username(db, username)
        status = user["status"]
        error_msg = user["error_msg"]
        if status == 418:
            return {"status": status, "error_msg": error_msg, "result": user["result"]}
        db_user = user_crud.change_user_state(db, username, state, action_user)
        if db_user is None:
            status = 418
            error_msg = 'change_user_state_failed'
    except (IntegrityError, FlushError) as exc:
        log.exception('%s - %s', exc, action_user)
        db.rollback()
        status = 418
        db_user = None
        error_msg = 'change_user_state_error'
    return {"status": status, "error_msg": error_msg, "result": db_user}


def get_user_by_username(db: Session, username):
    try:
        status = 200
        error_msg = ''
        db_user = user_crud.get_user_by_username(db, username)
        if db_user is None:
            status = 418
            error_msg = 'get_user_detail_by_username_failed'
    except (IntegrityError, FlushError) as exc:
        log.exception('%s', exc)
        status = 418
        db_user = None
        error_msg = 'get_user_detail_by_username_error'
    return {"status": status, "error_msg": error_msg, "result": db_user}


def get_user_list(db: Session):
    try:
        status = 200
        error_msg = ''
        db_user = user_crud.get_user_list(db)
        if db_user is None:
            status = 418
            error_msg = 'get_user_list_failed'
    except (IntegrityError, FlushError) as exc:
        log.exception('%s', exc)
        status = 418
        db_user = None
        error_msg = 'get_user_list_error'
    return {"status": status, "error_msg": error_msg, "result": db_user}


def get_user_active_list(db: Session):
    try:
        status = 200
        error_msg = ''
        db_user = user_crud.get_user_active_list(db)
        if db_user is None:
            status = 418
            error_msg = 'get_user_active_list_failed'
    except (IntegrityError, FlushError) as exc:
        log.exception('%s', exc)
        status = 418
        db_user = None
        error_msg = 'get_user_active_list_error'
    return {"status": status, "error_msg": error_msg, "result": db_user}


def search(db: Session, search_text):
    try:
        status = 200
        error_msg = ''
        if not search_text:
            search_text = ''
        db_user = user_crud.search(db, search_text)
        if db_user is None:
            status = 418
            error_msg = 'search_user_failed'
    except (IntegrityError, FlushError) as exc:
        log.exception('%s', exc)
        status = 418
        db_user = None
        error_msg = 'search_user_error'
    return {"status": status, "error_msg": error_msg, "result": db_user}


def search_active(db: Session, search_text):
    try:
        status = 200
        error_msg = ''
        if not search_text:
            search_text = ''
        db_user = user_crud.search_active(db, search_text)
        if db_user is None:
            status = 418
            error_msg = 'search_active_user_failed'
    except (IntegrityError, FlushError) as exc:
        log.exception('%s', exc)
        status = 418
        db_user = None
        error_msg = 'search_active_user_error'
    return {"status": status, "error_msg": error_msg, "result": db_user}


def get_user_action_log_list_by_username(db: Session, username):
    try:
        status = 200
        error_msg = ''
        db_user = user_crud.get_user_action_log_list_by_username(db, username)
    except (IntegrityError, FlushError) as exc:
        log.exception('%s', exc)
        status = 418
        db_user = None
        error_msg = 'get_user_action_log_list_by_username_error'
    return {"status": status, "error_msg": error_msg, "result": db_user}


def log_out(db: Session, username):
    try:
        status = 200
        error_msg = ''
        db_user = user_crud.add_user_action_log(db, username, models.UserAction.UserLogOut, None, None, None, None,
                                                None)
        if db_user is None:
            status = 418
            error_msg = 'user_log_out_failed'
    except (IntegrityError, FlushError) as exc:
        log.exception('%s', exc)
        status = 418
        error_msg = 'user_log_out_error'
    return {"status": status, "error_msg": error_msg, "result": None}


# endregion


# region Logs
def get_user_log_list_username(db: Session, username):
    try:
        status = 200
        error_msg = ''
        db_log = user_crud.get_user_log_list_username(db, username)
        if db_log is None:
            status = 418
            error_msg = 'get_user_log_list_username_failed'
    except (IntegrityError, FlushError) as exc:
        log.exception('%s', exc)
        status = 418
        db_log = None
        error_msg = 'get_user_log_list_username_error'
    return {"status": status, "error_msg": error_msg, "result": db_log}


def get_user_action_log_list_username(db: Session, username):
    try:
        status = 200
        error_msg = ''
        db_log = user_crud.get_user_action_log_list_username(db, username)
        if db_log is None:
            status = 418
            error_msg = 'get_user_action_log_list_user_action_id_failed'
    except (IntegrityError, FlushError) as exc:
        log.exception('%s', exc)
        status = 418
        db_log = None
        error_msg = 'get_user_action_log_list_user_action_id_error'
    return {"status": status, "error_msg": error_msg, "result": db_log}
# endregion
