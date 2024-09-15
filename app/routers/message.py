import logging
from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, Form, HTTPException, Request
from fastapi_jwt_auth import AuthJWT
from fastapi_pagination import Page, add_pagination, paginate
from sqlalchemy.orm import Session

from app import schemas, models
from app.accesses import note_access, token_access
from app.database import get_db
from app.lib import get_remote_ip

router = APIRouter()
log = logging.getLogger(__name__)


# region Notes
@router.post("/add/")
async def add_note(request: Request, note_title: str = Form(None), note_text: str = Form(None),
                   note_tags: List[str] = Form(...), db: Session = Depends(get_db),
                   current_user: schemas.Users = Depends(token_access.get_current_active_user),
                   authorize: AuthJWT = Depends()):
    authorize.jwt_required()
    log.debug("%s - Notes added - %s", current_user.username, get_remote_ip(request))

    note = await note_access.add_note(db, note_title=note_title, note_text=note_text, note_tags=note_tags,
                                      create_user=current_user.username)

    if note["status"] != 200:
        log.exception(note["error_msg"] + ' - %s - %s', current_user.username, get_remote_ip(request))
        raise HTTPException(status_code=note["status"], detail=note["error_msg"])
    else:
        db.commit()
    return note["result"]


@router.post("/edit/")
async def edit_note(request: Request, id: UUID = Form(...), note_title: str = Form(None), note_text: str = Form(None),
                    note_tags: List[str] = Form(...), db: Session = Depends(get_db),
                    current_user: schemas.Users = Depends(token_access.get_current_active_user),
                    authorize: AuthJWT = Depends()):
    authorize.jwt_required()
    log.debug("%s - Notes edited - %s", current_user.username, get_remote_ip(request))

    note = await note_access.edit_note(db, id=id, note_title=note_title, note_text=note_text, note_tags=note_tags,
                                       action_user=current_user.username)

    if note["status"] != 200:
        log.exception(note["error_msg"] + ' - %s - %s', current_user.username, get_remote_ip(request))
        raise HTTPException(status_code=note["status"], detail=note["error_msg"])
    else:
        db.commit()
    return note["result"]


@router.put("/change-state/{state}/")
def change_note_state(request: Request, state: models.EntityState, id: UUID = Form(...),
                      db: Session = Depends(get_db),
                      current_user: schemas.Users = Depends(token_access.get_current_active_user),
                      authorize: AuthJWT = Depends()):
    authorize.jwt_required()
    log.debug("%s - Notes note state changed - %s", current_user.username, get_remote_ip(request))

    note = note_access.change_note_state(db, id=id, state=state, action_user=current_user.username)

    if note["status"] != 200:
        log.exception(note["error_msg"] + ' - %s - %s', current_user.username, get_remote_ip(request))
        raise HTTPException(status_code=note["status"], detail=note["error_msg"])
    else:
        db.commit()
    return note["result"]


@router.get("/detail/{id}/", response_model=schemas.Notes)
def get_note_by_id(request: Request, id: UUID, db: Session = Depends(get_db),
                   current_user: schemas.Users = Depends(token_access.get_current_active_user),
                   authorize: AuthJWT = Depends()):
    authorize.jwt_required()
    log.debug("%s - Notes detail get by id - %s", current_user.username, get_remote_ip(request))

    note = note_access.get_note_by_id(db, id=id)

    if note["status"] != 200:
        log.exception(note["error_msg"] + ' - %s - %s', current_user.username, get_remote_ip(request))
        raise HTTPException(status_code=note["status"], detail=note["error_msg"])
    return note["result"]


@router.post("/search-active/", response_model=Page[schemas.Notes])
def search_active(request: Request, search_text: str = Form(None), db: Session = Depends(get_db),
                  current_user: schemas.Users = Depends(token_access.get_current_active_user),
                  authorize: AuthJWT = Depends()):
    authorize.jwt_required()
    log.debug("%s - Notes searched active - %s", current_user.username, get_remote_ip(request))

    note_list_view = note_access.search_active(db, search_text=search_text)

    if note_list_view["status"] != 200:
        log.exception(note_list_view["error_msg"] + ' - %s - %s', current_user.username, get_remote_ip(request))
        raise HTTPException(status_code=note_list_view["status"], detail=note_list_view["error_msg"])
    return paginate(note_list_view["result"])


@router.post("/search-active-by-user/", response_model=Page[schemas.Notes])
def search_active_by_user(request: Request, username: str = Form(...), search_text: str = Form(None),
                          db: Session = Depends(get_db),
                          current_user: schemas.Users = Depends(token_access.get_current_active_user),
                          authorize: AuthJWT = Depends()):
    authorize.jwt_required()
    log.debug("%s - Notes searched active by user - %s", current_user.username, get_remote_ip(request))

    note_list_view = note_access.search_active_by_user(db, username=username, search_text=search_text)

    if note_list_view["status"] != 200:
        log.exception(note_list_view["error_msg"] + ' - %s - %s', current_user.username, get_remote_ip(request))
        raise HTTPException(status_code=note_list_view["status"], detail=note_list_view["error_msg"])
    return paginate(note_list_view["result"])


# endregion


add_pagination(router)
