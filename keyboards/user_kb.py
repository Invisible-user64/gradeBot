from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from database.request import return_userlist, return_userlist_by_id

main_kb = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="🎯 Цели", callback_data="targets")],
                                                [InlineKeyboardButton(text="🗺️ Roadmaps", callback_data="roadmaps")],
                                                [InlineKeyboardButton(text="📚 МЭШ", callback_data="mes")],
                                                [InlineKeyboardButton(text="💼 Кворк", callback_data="kwork")],
                                                [InlineKeyboardButton(text="💡 Подсказка для успеха", callback_data="prompt")]])

targets_kb_test = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Создать цель", callback_data="create_target")],
                                                   [InlineKeyboardButton(text="Назад", callback_data="back")]])

async def create_targets_kb(tg_id):
    user_list = await return_userlist(tg_id=tg_id)
    
    buttons = [[InlineKeyboardButton(text="Создать цель", callback_data="create_target")]]

    for user in user_list:
        if not user.status:
            button_text = f"{user.title}  ❌"
            callback_data = f"target_{user.id}"
            buttons.append([InlineKeyboardButton(text=button_text, callback_data=callback_data)])

    buttons.append([InlineKeyboardButton(text="Выполненные цели", callback_data="execute_targets")])
    buttons.append([InlineKeyboardButton(text="Назад", callback_data="back")])

    targets_kb = InlineKeyboardMarkup(inline_keyboard=buttons)

    return targets_kb

async def create_execute_targets_kb(tg_id):
    user_list = await return_userlist(tg_id=tg_id)
    
    buttons = []

    for user in user_list:
        if user.status:
            button_text = f"{user.title}  ✅"
            callback_data = f"target_{user.id}"
            buttons.append([InlineKeyboardButton(text=button_text, callback_data=callback_data)])
            pass

    buttons.append([InlineKeyboardButton(text="Назад", callback_data="back_to_targets")])

    targets_kb = InlineKeyboardMarkup(inline_keyboard=buttons)

    return targets_kb


async def create_description_target_kb(id):
    user = await return_userlist_by_id(id)
    
    buttons = []

    if user.status:
        button_text = f"Цель ещё не выполнена ❌"
    else:
        button_text = f"Добился цели ✅"
    callback_data = f"click_target_{user.id}"
    buttons.append([InlineKeyboardButton(text=button_text, callback_data=callback_data)])

    buttons.append([InlineKeyboardButton(text="Назад", callback_data="back_to_targets")])

    targets_kb = InlineKeyboardMarkup(inline_keyboard=buttons)

    return targets_kb
