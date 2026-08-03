from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def get_main_menu():

    keyboard = [
        [InlineKeyboardButton("💰 قیمت ارزها", callback_data="menu:price")],
        [InlineKeyboardButton("⭐ واچ‌لیست", callback_data="menu:watchlist"), InlineKeyboardButton("🔔 هشدارها", callback_data="menu:alerts")],
        [InlineKeyboardButton("📊 پورتفولیو", callback_data="menu:portfolio")],
    ]
    return InlineKeyboardMarkup(keyboard)