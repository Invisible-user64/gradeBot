from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from keyboards.user_kb import create_roadmap_kb, create_show_roadmap_kb

from database.request import set_roadmap, show_roadmap, create_point

roadmap = Router()

@roadmap.callback_query(F.data == "roadmaps")
async def roadmaps(callback: CallbackQuery):
    tg_id = callback.from_user.id
    roadmap_kb = await create_roadmap_kb(tg_id)
    await callback.message.edit_text("Roadmaps - дорожные карты, или же то, чему вы хотите научиться подразбивая обучение на несколько элементов. Этот раздел нужен для объёмной информации.", reply_markup=roadmap_kb)
    await callback.answer("")

class Roadmap(StatesGroup):
    title = State()

@roadmap.callback_query(F.data == "create_roadmap")
async def create_roadmap(callback: CallbackQuery, state: FSMContext):
    await state.set_state(Roadmap.title)
    await callback.message.answer("Введите заголовок:")
    await callback.answer("")

@roadmap.message(Roadmap.title)
async def set_title(message: Message, state: FSMContext):
    text = message.text
    tg_id = message.from_user.id
    await state.update_data(title=text)
    data = await state.get_data()
    title = data["title"]
    await set_roadmap(tg_id, title)
    await message.answer("Вы успешно создали roadmap!")
    await state.clear()
    roadmap_kb = await create_roadmap_kb(tg_id)
    await message.answer("Roadmaps - дорожные карты, или же то, чему вы хотите научиться подразбивая обучение на несколько элементов. Этот раздел нужен для объёмной информации.", reply_markup=roadmap_kb)

@roadmap.callback_query(F.data.startswith("roadmap_"))
async def show_one_roadmap(callback: CallbackQuery):
    id = callback.data.split("_")[1]
    roadmap = await show_roadmap(id)
    title = roadmap.title
    show_roadmap_kb = await create_show_roadmap_kb(id)
    await callback.message.edit_text(f"{title}", reply_markup=show_roadmap_kb)
    await callback.answer("")

class Point(StatesGroup):
    id = State()

@roadmap.callback_query(F.data.startswith("create_point_"))
async def create_one_point(callback: CallbackQuery, state: FSMContext):
    id = callback.data.split("_")[2]
    await state.set_state(Point.id)
    await state.update_data(id = id)
    await callback.message.answer("Введите заголовок для пункта:")
    await callback.answer("")
    
@roadmap.message(Point.id)
async def point_title(message: Message, state: FSMContext):
    data = await state.get_data()
    id = data["id"]
    text = message.text
    await create_point(id, text)
    await message.answer("Вы создали пункт!")
    await state.clear()
    roadmap = await show_roadmap(id)
    title = roadmap.title
    show_roadmap_kb = await create_show_roadmap_kb(id)
    await message.answer(f"{title}", reply_markup=show_roadmap_kb)
