import logging
import httpx

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from sqlalchemy.orm import Session
from fastapi import Depends

from app import models
from app.accesses import user_access
from app.database import get_db

API_TOKEN = '7522077708:AAERLFHMGC6lvf93ijcVvGq8hU7FzNzoCJc'
API_BASE_URL = 'http://127.0.0.1:8000'

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())


# Авторизация пользователя
@dp.message_handler(commands=['start'])
async def start(message: types.Message, db: Session = Depends(get_db)):
    telegram_id = message.from_user.id
    username = message.from_user.username
    password = message.from_user.password
    fullname = message.from_user.fullname

    user = user_access.get_user_by_username(db, username)

    if user is None:
        user_access.add_user(db, username, password, models.UserRole.user, fullname, "admin")
        await message.reply(f"User {username} registered!")
    else:
        await message.reply(f"User with {username} already registered!")


# Получение списка заметок
@dp.message_handler(commands=['notes'])
async def get_notes(message: types.Message):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{API_BASE_URL}/notes/")
    notes = response.json()
    if notes:
        notes_list = "\n".join([f"{note['title']}: {note['content']}" for note in notes])
        await message.reply(f"Ваши заметки:\n{notes_list}")
    else:
        await message.reply("У вас нет заметок.")


# Создание новой заметки
@dp.message_handler(commands=['new_note'])
async def new_note_command(message: types.Message):
    await message.reply("Введите заголовок заметки:")

    @dp.message_handler()
    async def receive_title(msg: types.Message):
        title = msg.text
        await msg.reply("Введите содержание заметки:")

        @dp.message_handler()
        async def receive_content(content_msg: types.Message):
            content = content_msg.text
            await content_msg.reply("Введите теги через запятую:")

            @dp.message_handler()
            async def receive_tags(tags_msg: types.Message):
                tags = tags_msg.text.split(",")
                note_data = {"title": title, "content": content, "tags": tags}

                async with httpx.AsyncClient() as client:
                    await client.post(f"{API_BASE_URL}/notes/", json=note_data)

                await tags_msg.reply("Заметка успешно создана!")


# Поиск заметок по тегам
@dp.message_handler(commands=['search_note'])
async def search_note_command(message: types.Message):
    await message.reply("Введите теги через запятую для поиска:")

    @dp.message_handler()
    async def receive_tags(msg: types.Message):
        tags = msg.text
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{API_BASE_URL}/notes/search/?tags={tags}")

        notes = response.json()
        if notes:
            notes_list = "\n".join([f"{note['title']}: {note['content']}" for note in notes])
            await msg.reply(f"Заметки по тегам:\n{notes_list}")
        else:
            await msg.reply("Заметки по данным тегам не найдены.")


async def start_bot():
    await dp.start_polling()
