from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from database.request import return_userlist, return_userlist_by_id, return_roadmap_list, show_roadmap, get_point

main_kb = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="🎯 Цели", callback_data="targets")],
                                                [InlineKeyboardButton(text="🗺️ Roadmaps", callback_data="roadmaps")],
                                                [InlineKeyboardButton(text="📚 МЭШ", callback_data="mes")],
                                                [InlineKeyboardButton(text="💼 Кворк", callback_data="kwork")],
                                                [InlineKeyboardButton(text="💡 Подсказка для успеха", callback_data="prompt")]])


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

    buttons.append([InlineKeyboardButton(text="Назад", callback_data="targets")])

    targets_kb = InlineKeyboardMarkup(inline_keyboard=buttons)

    return targets_kb


async def create_description_target_kb(id):
    user = await return_userlist_by_id(id)
    
    buttons = []

    if user.status:
        button_text = f"❌ Цель ещё не выполнена"
    else:
        button_text = f"✅ Добился цели"
    callback_data = f"click_target_{user.id}"
    buttons.append([InlineKeyboardButton(text=button_text, callback_data=callback_data)])

    buttons.append([InlineKeyboardButton(text="🗑️ Удалить цель", callback_data=f"delete_target_{id}")])

    if user.status:
        buttons.append([InlineKeyboardButton(text="Назад", callback_data="execute_targets")])
    else:
        buttons.append([InlineKeyboardButton(text="Назад", callback_data="targets")])

    targets_kb = InlineKeyboardMarkup(inline_keyboard=buttons)

    return targets_kb

async def create_roadmap_kb(tg_id):
    roadmap_list = await return_roadmap_list(tg_id)

    buttons = [[InlineKeyboardButton(text="Создать roadmap", callback_data="create_roadmap")]]

    for roadmap in roadmap_list:
        button_text = f"{roadmap.title}"
        button_callback = f"roadmap_{roadmap.id}"
        buttons.append({InlineKeyboardButton(text=button_text, callback_data=button_callback)})

    buttons.append([InlineKeyboardButton(text="Назад", callback_data="back")])
    
    roadmap_kb = InlineKeyboardMarkup(inline_keyboard=buttons)
    return roadmap_kb

async def create_show_roadmap_kb(id):
    roadmap = await show_roadmap(id)
    json_list = roadmap.point

    buttons = []

    for index, json in enumerate(json_list):
        text = json["title"]
        status = json["status"]
        status_text = None
        if status:
            status_text = "✅"
        else:
            status_text = "❌"

        buttons.append([InlineKeyboardButton(text=f"{text} {status_text}", callback_data=f"point_{id}_{index}")])

    buttons.append([InlineKeyboardButton(text="Создать пункт", callback_data=f"create_point_{id}")])
    buttons.append([InlineKeyboardButton(text="Удалить Roadmap", callback_data=f"delete_roadmap_{id}")])
    buttons.append([InlineKeyboardButton(text="Назад", callback_data="roadmaps")])
    show_roadmap_kb = InlineKeyboardMarkup(inline_keyboard=buttons)

    return show_roadmap_kb

async def create_point_kb(id, index):
    point = await get_point(id, index)
    status = point["status"]
    status_text = None
    buttons = []
    if status:
        status_text = "Пункт ещё не выполнен ❌"  
    else:
        status_text = "Выполнить ✅"
    
    buttons.append([InlineKeyboardButton(text=status_text, callback_data=f"change_point_{id}_{index}")])
    buttons.append([InlineKeyboardButton(text="Удалить пункт", callback_data=f"delete_point_{id}_{index}")])
    buttons.append([InlineKeyboardButton(text="Назад", callback_data=f"roadmap_{id}")])

    point_kb = InlineKeyboardMarkup(inline_keyboard=buttons)

    return point_kb


