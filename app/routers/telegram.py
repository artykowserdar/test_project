import asyncio
import logging

from fastapi import (APIRouter)

from app.telegram import bot

router = APIRouter()
log = logging.getLogger(__name__)


# region Users
@router.on_event("/bot-startup/")
async def startup():
    await asyncio.create_task(bot.start_bot())
