import logging
from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

from app import config, models
from app.accesses import token_access, user_access
from app.cruds import user_crud
from app.database import get_db
from app.lib import get_remote_ip

router = APIRouter()
log = logging.getLogger(__name__)


@router.post("/token/")
async def login_for_access_token(request: Request, form_data: OAuth2PasswordRequestForm = Depends(),
                                 db: Session = Depends(get_db), authorize: AuthJWT = Depends()):
    user = token_access.authenticate_user(db, form_data.username, form_data.password)
    log.debug('%s: token request: %s', form_data.username, get_remote_ip(request))
    try:
        if not user:
            raise HTTPException(
                status_code=401,
                detail="Неверное имя пользователя или пароль",
                headers={"WWW-Authenticate": "Bearer"},
            )
        access_token_expires = timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = authorize.create_access_token(subject=user.username, expires_time=access_token_expires)
        refresh_token = authorize.create_refresh_token(subject=user.username)
        user_crud.add_user_action_log(db, user.username, models.UserAction.UserLogIn, None, None, None, None, None)
    except Exception:
        log.exception("%s - Error token request - %s", form_data.username, get_remote_ip(request))
        raise HTTPException(status_code=404, detail="ERROR")
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer", "role": user.role,
            "username": user.username, "fullname": user.fullname}


@router.post("/refresh/")
async def refresh_token(request: Request, authorize: AuthJWT = Depends(), db: Session = Depends(get_db)):
    authorize.jwt_refresh_token_required()
    current_user = authorize.get_jwt_subject()
    user = token_access.authenticate_user_with_refresh_token(db, current_user)
    try:
        if not user:
            raise HTTPException(
                status_code=401,
                detail="Incorrect username",
                headers={"WWW-Authenticate": "Bearer"},
            )
        access_token_expires = timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)
        new_access_token = authorize.create_access_token(subject=user.username, expires_time=access_token_expires)
        refresh_token = authorize.create_refresh_token(subject=user.username)
    except Exception:
        log.exception("%s - Error token request - %s", current_user, get_remote_ip(request))
        raise HTTPException(status_code=404, detail="ERROR")
    return {"access_token": new_access_token, "refresh_token": refresh_token, "token_type": "bearer",
            "role": user.role, "username": user.username, "fullname": user.fullname}


@router.get('/protected/')
def protected(authorize: AuthJWT = Depends()):
    authorize.jwt_required()

    current_user = authorize.get_jwt_subject()
    return {"user": current_user}


@router.post("/add-temp-users/")
def add_temp_users(request: Request, db: Session = Depends(get_db)):
    log.debug("%s - Temp users added - %s", get_remote_ip(request))
    user_access.add_user(db,
                         username="system",
                         password="system",
                         role=models.UserRole.system,
                         fullname="SYSTEM",
                         action_user=None)
    user_access.add_user(db,
                         username="admin",
                         password="admin",
                         role=models.UserRole.admin,
                         fullname="ADMIN",
                         action_user=None)
    db.commit()
    return True
