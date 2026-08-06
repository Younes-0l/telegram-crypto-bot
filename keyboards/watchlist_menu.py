from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def get_watchlist_menu(entries: list[dict]) -> InlineKeyboardMarkup:
    keyboard = []

    for entry in entries:
        price_text = f"{entry['price']:,.0f}" if entry['price'] is not None else "نامشخص"
        symbol = entry["symbol"]
        row = [
            InlineKeyboardButton(f"{symbol}: {price_text} تومان", callback_data=f"noop"),
            InlineKeyboardButton("❌", callback_data=f"watchlist_remove:{symbol}"),
        ]
        keyboard.append(row)

    keyboard.append([InlineKeyboardButton("افزودن ارز ➕", callback_data="watchlist_add")])
    keyboard.append([InlineKeyboardButton("بازگشت 🔙", callback_data="back:main")])

    return InlineKeyboardMarkup(keyboard)


def get_empty_watchlist_menu() -> InlineKeyboardMarkup:
    keyboard = [
        [InlineKeyboardButton("افزودن ارز ➕", callback_data="watchlist_add")],
        [InlineKeyboardButton("بازگشت 🔙", callback_data="back:main")],
    ]
    return InlineKeyboardMarkup(keyboard)