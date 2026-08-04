# handlers/navigation.py
from telegram import Update
from telegram.ext import ContextTypes
from keyboards.main_menu import get_main_menu
from keyboards.coin_menu import get_coin_selection_menu


MENU_MAP = {
    "main": ("منوی اصلی رو انتخاب کن:", get_main_menu),
    "price_menu": ("ارز موردنظرت رو انتخاب کن:", get_coin_selection_menu),
}


async def go_back(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    target = query.data.split(":")[1]

    await query.answer()

    menu_data = MENU_MAP.get(target)
    if not menu_data:
        text, keyboard_fn = MENU_MAP["main"]
    else:
        text, keyboard_fn = menu_data

    await query.message.edit_text(text, reply_markup=keyboard_fn())