from aiogram import Bot, Dispatcher
from aiogram.filters.command import Command
import asyncio
import logging
import aiogram

from app.utils import generate_token
from app.settings import AppSettings


from aiogram import Bot, Dispatcher
from aiogram.filters.command import Command
import aiogram
import logging
from app.auth.dao import UserDAO
from app.auth.utils import get_password_hash
from app.settings import AppSettings


tokens_map = {}


logging.basicConfig(level=logging.INFO)
bot = Bot(token=AppSettings.TELEGRAM_BOT_TOKEN)
dp = Dispatcher()


@dp.message(Command(commands=["/r", "/register"]))
async def cmd_start(message: aiogram.types.Message):
    user_id = message.from_user.id
    new_token = generate_token()
    if user_id in tokens_map:
        await message.answer('Вы уже были зарегистрированы')
    else:
        tokens_map[user_id] = new_token
        registration_link = f"{AppSettings.BASE_URL}/auth/me/activate?reset_token={new_token}"
        await message.answer(f'Вот ваша ссылка для регестрации: {registration_link}')





if __name__ == '__main__':
    dp.run_polling(bot)
