import datetime
import json
import uuid
from datetime import datetime

from sqlalchemy import func
from sqlalchemy.orm import Session

from app import models


# region Notes
def add_note(db: Session, note_title, note_text, note_tags, create_user):
    db_note = models.Notes(id=uuid.uuid4(),
                           note_title=note_title,
                           note_text=note_text,
                           note_tags=note_tags,
                           create_user=create_user,
                           state=models.EntityState.active,
                           create_ts=datetime.now(),
                           update_ts=datetime.now())
    db.add(db_note)
    db.flush()
    note_json_info = {'note_title': str(note_title),
                      'note_text': str(note_text),
                      'note_tags': str(note_tags),
                      'create_user': str(create_user)}
    db_note_log = models.NoteLog(id=uuid.uuid4(),
                                 note_id=db_note.id,
                                 action=models.NoteAction.NoteAdd,
                                 action_user=create_user,
                                 sup_info=json.dumps(note_json_info),
                                 action_ts=datetime.now())
    db.add(db_note_log)
    return db_note.id


def edit_note(db: Session, id, note_title, note_text, note_tags, action_user):
    db_note = db.query(models.Notes).filter(models.Notes.id == id)
    edit_note_crud = {
        models.Notes.note_title: note_title,
        models.Notes.update_ts: datetime.now()
    }
    db_note.update(edit_note_crud)
    note_json_info = {'note_title': str(note_title),
                      'note_text': str(note_text),
                      'note_tags': str(note_tags)}
    db_note_log = models.NoteLog(id=uuid.uuid4(),
                                 note_id=id,
                                 action=models.NoteAction.NoteEdit,
                                 action_user=action_user,
                                 sup_info=json.dumps(note_json_info),
                                 action_ts=datetime.now())
    db.add(db_note_log)
    return id


def change_note_state(db: Session, id, state, action_user):
    db_note = db.query(models.Notes).filter(models.Notes.id == id)
    edit_note_crud = {
        models.Notes.state: state,
        models.Notes.update_ts: datetime.now()
    }
    db_note.update(edit_note_crud)
    note_json_info = {'state': str(state)}
    db_note_log = models.NoteLog(id=uuid.uuid4(),
                                 note_id=id,
                                 action=models.NoteAction.NoteStateChange,
                                 action_user=action_user,
                                 sup_info=json.dumps(note_json_info),
                                 action_ts=datetime.now())
    db.add(db_note_log)
    return id


def get_note_by_id(db: Session, id):
    db_note = db.query(models.Notes).get(id)
    return db_note


def search_active(db: Session, search_text):
    db_note = db.query(models.Notes) \
        .filter(models.Notes.state == models.EntityState.active) \
        .filter(func.concat(models.Notes.note_title,
                            ' ', func.array_to_string(models.Notes.note_tags, ','),
                            ' ', func.to_char(models.Notes.create_ts, "DD.MM.YYYY"))
                .ilike('%' + search_text + '%')) \
        .order_by(models.Notes.create_ts.desc())
    return db_note.all()


def search_active_by_user(db: Session, username, search_text):
    db_note = db.query(models.Notes) \
        .filter(models.Notes.state == models.EntityState.active) \
        .filter(models.Notes.create_user == username) \
        .filter(func.concat(models.Notes.note_title,
                            ' ', func.array_to_string(models.Notes.note_tags, ','),
                            ' ', func.to_char(models.Notes.create_ts, "DD.MM.YYYY"))
                .ilike('%' + search_text + '%')) \
        .order_by(models.Notes.create_ts.desc())
    return db_note.all()

# endregion
