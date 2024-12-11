import logging
import asyncio

import aiogram
from aiogram import Bot, Dispatcher
from aiogram.filters.command import Command

from pydantic import create_model

from app.settings import get_settings
from app.auth.dao import UserDAO
from app.dao.session import session_manager


settings = get_settings()

logging.basicConfig(level=logging.INFO)
bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def cmd_start(message: aiogram.types.Message):
    await message.answer('👋')
    await message.answer(f'Ваш Telegram ID: {message.from_user.id}')

@dp.message(Command("get_id"))
async def get_id(message: aiogram.types.Message):
    await message.answer(f'Ваш Telegram ID: {message.from_user.id}')


@dp.message(Command("register"))
async def register(message: aiogram.types.Message):
    db_session = session_manager.session_maker()
    ValuesModel = create_model('ValuesModel', telegram_id=(int, ...))
    user = await UserDAO.find_one_or_none(db_session, ValuesModel(telegram_id=message.from_user.id))
    await db_session.close()
    if user:
        if user.completed_registration:
            await message.answer('Вы уже зарегистрированы')
            return
        elif user.disabled:
            await message.answer('Ваш аккаунт деактивирован')
            return
        elif not user.completed_registration:
            registration_link = f"{settings.ROOT_URL}auth/me/activate?reset_token={user.reset_token}"
            await message.answer(f'Ваша ссылка для регистрации: {registration_link}')
    else:
        await message.answer('🤷‍♂️')


@dp.message(Command("reset"))
async def reset_password(message: aiogram.types.Message):
    db_session = session_manager.session_maker()
    ValuesModel = create_model('ValuesModel', telegram_id=(int, ...))
    user = await UserDAO.find_one_or_none(db_session, ValuesModel(telegram_id=message.from_user.id))
    await db_session.close()
    if user:
        if user.disabled:
            await message.answer('Ваш аккаунт деактивирован')
            return
        elif not user.completed_registration:
            reset_password_link = f"{settings.ROOT_URL}auth/me/activate?reset_token={user.reset_token}"
            await message.answer(f'Ваша ссылка для сброса пароля: {reset_password_link}')
    else:
        await message.answer('🤷‍♂️')


@dp.message(Command("deactivate"))
async def deactivate(message: aiogram.types.Message):
    db_session = session_manager.session_maker()
    ValuesModel = create_model('ValuesModel', telegram_id=(int, ...))
    user = await UserDAO.find_one_or_none(db_session, ValuesModel(telegram_id=message.from_user.id))
    await db_session.close()
    if user:
        if user.disabled:
            await message.answer('Ваш аккаунт уже был деактивирован')
            return
        else:
            reset_password_link = f"{settings.ROOT_URL}auth/me/deactivate?reset_token={user.reset_token}"
            await message.answer(f'Ваша ссылка для сброса пароля: {reset_password_link}')
    else:
        await message.answer('🤷‍♂️')

async def bot_start_polling():
    await dp.start_polling(bot)

async def bot_stop_polling():
    await dp.stop_polling()

# async def bot_start_polling():
#     try:
#         asyncio.create_task()
#         # executor.start_polling(bot, allowed_updates=dp.resolve_used_update_types(), skip_updates=True)
#     finally:
#         await dp.stop_polling()