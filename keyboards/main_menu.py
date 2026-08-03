from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_main_menu():
    kb = InlineKeyboardBuilder()
    kb.button(text="💰 قیمت ارزها", callback_data="menu:price")
    kb.button(text="⭐ واچ‌لیست", callback_data="menu:watchlist")
    kb.button(text="🔔 هشدارها", callback_data="menu:alerts")
    kb.button(text="📊 پورتفولیو", callback_data="menu:portfolio")
    kb.adjust(2)
    return kb.as_markup()