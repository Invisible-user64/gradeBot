from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart

from keyboards.user_kb import main_kb

from database.request import set_user

user = Router()

@user.message(CommandStart())
async def cmd_start(message: Message):
    tg_id = message.from_user.id
    await set_user(tg_id)
    await message.answer("Привет, я бот для улучшения твоей успеваемости! Здесь ты сможешь менять самого себя!", reply_markup=main_kb)

@user.callback_query(F.data == "back")
async def back_to_menu(callback: CallbackQuery):
    await callback.message.edit_text("Главное меню:", reply_markup=main_kb)
    await callback.answer("")