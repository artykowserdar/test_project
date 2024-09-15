import logging

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import FlushError

from app.cruds import note_crud

log = logging.getLogger(__name__)


# region Notes
async def add_note(db: Session, note_title, note_text, note_tags, create_user):
    try:
        status = 200
        error_msg = ''
        db_note = note_crud.add_note(db, note_title, note_text, note_tags, create_user)
        if db_note is None:
            status = 418
            error_msg = 'add_note_failed'
    except (IntegrityError, FlushError) as exc:
        log.exception('%s - %s', exc, create_user)
        db.rollback()
        status = 418
        db_note = None
        error_msg = 'add_note_error'
    return {"status": status, "error_msg": error_msg, "result": db_note}


async def edit_note(db: Session, id, note_title, note_text, note_tags, action_user):
    try:
        status = 200
        error_msg = ''
        db_note = note_crud.edit_note(db, id, note_title, note_text, note_tags, action_user)
        if db_note is None:
            status = 418
            error_msg = 'edit_note_failed'
    except (IntegrityError, FlushError) as exc:
        log.exception('%s - %s', exc, action_user)
        db.rollback()
        status = 418
        db_note = None
        error_msg = 'edit_note_error'
    return {"status": status, "error_msg": error_msg, "result": db_note}


def change_note_state(db: Session, id, state, action_user):
    try:
        status = 200
        error_msg = ''
        db_note = note_crud.change_note_state(db, id, state, action_user)
        if db_note is None:
            status = 418
            error_msg = 'change_note_state_failed'
    except (IntegrityError, FlushError) as exc:
        log.exception('%s - %s', exc, action_user)
        db.rollback()
        status = 418
        db_note = None
        error_msg = 'change_note_state_error'
    return {"status": status, "error_msg": error_msg, "result": db_note}


def get_note_by_id(db: Session, id):
    try:
        status = 200
        error_msg = ''
        db_note = note_crud.get_note_by_id(db, id)
        if db_note is None:
            status = 418
            error_msg = 'get_note_detail_by_id_failed'
    except (IntegrityError, FlushError) as exc:
        log.exception('%s', exc)
        status = 418
        db_note = None
        error_msg = 'get_note_detail_by_id_error'
    return {"status": status, "error_msg": error_msg, "result": db_note}


def search_active(db: Session, search_text):
    try:
        status = 200
        error_msg = ''
        if not search_text:
            search_text = ''
        db_note = note_crud.search_active(db, search_text)
        if db_note is None:
            status = 418
            error_msg = 'search_active_failed'
    except (IntegrityError, FlushError) as exc:
        log.exception('%s', exc)
        status = 418
        db_note = None
        error_msg = 'search_active_error'
    return {"status": status, "error_msg": error_msg, "result": db_note}


def search_active_by_user(db: Session, username, search_text):
    try:
        status = 200
        error_msg = ''
        if not search_text:
            search_text = ''
        db_note = note_crud.search_active_by_user(db, username, search_text)
        if db_note is None:
            status = 418
            error_msg = 'search_active_by_user_failed'
    except (IntegrityError, FlushError) as exc:
        log.exception('%s', exc)
        status = 418
        db_note = None
        error_msg = 'search_active_by_user_error'
    return {"status": status, "error_msg": error_msg, "result": db_note}


# endregion
