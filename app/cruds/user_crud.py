import json
import uuid
from datetime import datetime

from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy import func
from sqlalchemy.orm import Session

from app import models


# region Samples


# endregion


# region Users
def add_user(db: Session, username, hash_password, role, fullname, action_user):
    db_user = models.Users(username=username,
                           fullname=fullname,
                           hashed_password=hash_password,
                           role=role,
                           state=models.UserState.enabled.name,
                           create_ts=datetime.now(),
                           update_ts=datetime.now())
    db.add(db_user)
    db.flush()
    if action_user:
        user_json_info = {'username': username,
                          'role': role,
                          'fullname': fullname}
        db_user_log = models.UserLog(id=uuid.uuid4(),
                                     username=username,
                                     action=models.UserAction.UserCreate,
                                     action_user=action_user,
                                     sup_info=json.dumps(user_json_info),
                                     action_ts=datetime.now())
        db.add(db_user_log)
    return username


def edit_user(db: Session, username, role, fullname, action_user):
    db_user = db.query(models.Users).filter(models.Users.username == username)
    edit_user_crud = {
        models.Users.role: role,
        models.Users.fullname: fullname,
        models.Users.update_ts: datetime.now()
    }
    db_user.update(edit_user_crud)
    user_json_info = {'username': username,
                      'role': role,
                      'fullname': fullname}
    db_user_log = models.UserLog(id=uuid.uuid4(),
                                 username=username,
                                 action=models.UserAction.UserEdit,
                                 action_user=action_user,
                                 sup_info=json.dumps(user_json_info),
                                 action_ts=datetime.now())
    db.add(db_user_log)
    return username


def change_user_password(db: Session, username, hash_password, action_user):
    db_user = db.query(models.Users).filter(models.Users.username == username)
    edit_user_crud = {
        models.Users.hashed_password: hash_password,
        models.Users.update_ts: datetime.now()
    }
    db_user.update(edit_user_crud)
    if action_user:
        user_json_info = {'username': username}
        db_user_log = models.UserLog(id=uuid.uuid4(),
                                     username=username,
                                     action=models.UserAction.UserChangePassword,
                                     action_user=action_user,
                                     sup_info=json.dumps(user_json_info),
                                     action_ts=datetime.now())
        db.add(db_user_log)
    return username


def change_user_role(db: Session, username, role, action_user):
    db_user = db.query(models.Users).filter(models.Users.username == username)
    edit_user_crud = {
        models.Users.role: role,
        models.Users.update_ts: datetime.now()
    }
    db_user.update(edit_user_crud)
    user_json_info = {'username': username,
                      'role': role.name}
    db_user_log = models.UserLog(id=uuid.uuid4(),
                                 username=username,
                                 action=models.UserAction.UserRoleChange,
                                 action_user=action_user,
                                 sup_info=json.dumps(user_json_info),
                                 action_ts=datetime.now())
    db.add(db_user_log)
    return username


def change_user_state(db: Session, username, state, action_user):
    db_user = db.query(models.Users).filter(models.Users.username == username)
    edit_user_crud = {
        models.Users.state: state,
        models.Users.update_ts: datetime.now()
    }
    db_user.update(edit_user_crud)
    if action_user:
        user_json_info = {'username': username,
                          'state': state.name}
        db_user_log = models.UserLog(id=uuid.uuid4(),
                                     username=username,
                                     action=models.UserAction.UserStateChange,
                                     action_user=action_user,
                                     sup_info=json.dumps(user_json_info),
                                     action_ts=datetime.now())
        db.add(db_user_log)
    return username


def get_user_by_username(db: Session, username):
    db_user = db.query(models.Users) \
        .filter(models.Users.username == username)
    return db_user.first()


def get_user_detail_by_username(db: Session, username):
    query = db.query(models.Users) \
        .filter(models.Users.username == username)
    return query.first()


def get_active_user_by_username(db: Session, username):
    query = db.query(models.Users) \
        .filter(models.Users.username == username) \
        .filter(models.Users.state == models.UserState.enabled)
    return query.first()


def get_user_list(db: Session):
    query = db.query(models.Users) \
        .filter(models.Users.role != models.UserRole.system)
    return query.all()


def get_user_active_list(db: Session):
    query = db.query(models.Users) \
        .filter(models.Users.state == models.UserState.enabled) \
        .filter(models.Users.role != models.UserRole.system)
    return query.all()


def search(db: Session, search_text):
    query = db.query(models.Users) \
        .filter(models.Users.role != models.UserRole.system) \
        .filter(models.Users.username.ilike('%' + search_text + '%')) \
        .order_by(models.Users.username)
    return query.all()


def search_active(db: Session, search_text):
    query = db.query(models.Users) \
        .filter(models.Users.role != models.UserRole.system) \
        .filter(models.Users.state != models.UserState.deleted) \
        .filter(func.concat(models.Users.username,
                            ' ', models.Users.fullname
                            ).ilike('%' + search_text + '%')) \
        .order_by(models.Users.username)
    return query.all()


def get_user_action_log_list_by_username(db: Session, username):
    query = db.query(models.UserActionLog) \
        .filter(models.Users.username == username).all()
    return paginate(query)


# endregion


# region Logs
def add_user_action_log(db: Session, username, action, action_user, cash_register_id, restaurant_id, pay_total, items):
    user_action_json_info = {'action_user': action_user,
                             'cash_register_id': str(cash_register_id),
                             'restaurant_id': str(restaurant_id),
                             'pay_total': str(pay_total)}
    db_user_action_log = models.UserActionLog(id=uuid.uuid4(),
                                              username=username,
                                              action=action,
                                              sup_info=json.dumps(user_action_json_info),
                                              items=items,
                                              action_ts=datetime.now())
    db.add(db_user_action_log)
    return username


def get_user_log_list_username(db: Session, username):
    db_log = db.query(models.UserLog) \
        .filter(models.UserLog.username == username).all()
    return db_log


def get_user_action_log_list_username(db: Session, username):
    db_log = db.query(models.UserActionLog) \
        .filter(models.UserActionLog.username == username).all()
    return db_log
# endregion
