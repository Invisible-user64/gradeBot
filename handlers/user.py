from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from keyboards.user_kb import main_kb, create_targets_kb, create_description_target_kb, create_execute_targets_kb

from database.request import set_user, set_targets, return_userlist_by_id, change_target_status

user = Router()

@user.message(CommandStart())
async def cmd_start(message: Message):
    tg_id = message.from_user.id
    await set_user(tg_id)
    await message.answer("Привет, я бот для улучшения твоей успеваемости! Здесь ты сможешь менять самого себя!", reply_markup=main_kb)

@user.callback_query(F.data == "targets")
async def targets(callback: CallbackQuery):
    tg_id = callback.from_user.id
    targets_kb = await create_targets_kb(tg_id)
    await callback.message.edit_text("Цели - это что-то очень важное и большое, поэтому этот раздел сделан для того, чтобы писать сюда то, что будет выполняться в течение долгого времени.", reply_markup=targets_kb)
    await callback.answer("")

@user.callback_query(F.data == "back")
async def back_to_menu(callback: CallbackQuery):
    await callback.message.edit_text("Главное меню:", reply_markup=main_kb)
    await callback.answer("")

class Target(StatesGroup):
    title = State()
    description = State()

@user.callback_query(F.data == "create_target")
async def create_targets(callback: CallbackQuery, state: FSMContext):
    await state.set_state(Target.title)
    await callback.message.edit_text("Введите заголовок:")
    await callback.answer("")

@user.message(Target.title)
async def target_title(message: Message, state: FSMContext):
    text = message.text
    await state.update_data(title=text)
    await state.set_state(Target.description)
    await message.answer("Введите описание цели:")

@user.message(Target.description)
async def target_description(message: Message, state: FSMContext):
    text = message.text
    tg_id = message.from_user.id
    await state.update_data(description=text)
    data = await state.get_data()
    title = data["title"]
    description = data["description"]
    await set_targets(tg_id, title, description)
    await message.answer("Вы создали цель!")
    targets_kb = await create_targets_kb(tg_id)
    await message.answer("Цели - это что-то очень важное и большое, поэтому этот раздел сделан для того, чтобы писать сюда то, что будет выполняться в течение долгого времени.", reply_markup=targets_kb)

@user.callback_query(F.data.startswith("target_"))
async def show_target(callback: CallbackQuery):
    id = int(callback.data.split("_")[1])
    target = await return_userlist_by_id(id)
    title = target.title
    description = target.description
    status = target.status
    status_view = None
    description_target_kb = await create_description_target_kb(id)
    if status:
        status_view = "Выполнена ✅"
    else:
        status_view = "Не выполнена ❌"
    await callback.message.edit_text(f"{title}\n\n{description}\nСтатус: {status_view}", reply_markup=description_target_kb)
    await callback.answer("")

@user.callback_query(F.data == "execute_targets")
async def show_execute_target(callback: CallbackQuery):
    tg_id = callback.from_user.id
    targets_kb = await create_execute_targets_kb(tg_id)
    await callback.message.edit_text("Цели - это что-то очень важное и большое, поэтому этот раздел сделан для того, чтобы писать сюда то, что будет выполняться в течение долгого времени.", reply_markup=targets_kb)
    await callback.answer("")

@user.callback_query(F.data == "back_to_targets")
async def back_to_targets(callback: CallbackQuery):
    tg_id = callback.from_user.id
    targets_kb = await create_targets_kb(tg_id)
    await callback.message.edit_text("Цели - это что-то очень важное и большое, поэтому этот раздел сделан для того, чтобы писать сюда то, что будет выполняться в течение долгого времени.", reply_markup=targets_kb)
    await callback.answer("")

@user.callback_query(F.data.startswith("click_target_"))
async def change_status(callback: CallbackQuery):
    id = int(callback.data.split("_")[2])
    await change_target_status(id)
    target = await return_userlist_by_id(id)
    title = target.title
    description = target.description
    status = target.status
    status_view = None
    description_target_kb = await create_description_target_kb(id)
    if status:
        status_view = "Выполнена ✅"
    else:
        status_view = "Не выполнена ❌"
    await callback.message.edit_text(f"{title}\n\n{description}\nСтатус: {status_view}", reply_markup=description_target_kb)
    await callback.answer("")