from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def get_portfolio_menu(holdings: list) -> InlineKeyboardMarkup:
    keyboard = []
    for h in holdings:
        row = [
            InlineKeyboardButton(f"{h['symbol']}: {h['amount']:g}", callback_data="noop"),
            InlineKeyboardButton("✏️", callback_data=f"holding_edit:{h['symbol']}"),
            InlineKeyboardButton("❌", callback_data=f"holding_remove:{h['symbol']}"),
        ]
        keyboard.append(row)
    keyboard.append([InlineKeyboardButton("افزودن دارایی ➕", callback_data="holding_add")])
    keyboard.append([InlineKeyboardButton("بازگشت 🔙", callback_data="back:main")])
    return InlineKeyboardMarkup(keyboard)


def get_empty_portfolio_menu() -> InlineKeyboardMarkup:
    keyboard = [
        [InlineKeyboardButton("افزودن دارایی ➕", callback_data="holding_add")],
        [InlineKeyboardButton("بازگشت 🔙", callback_data="back:main")],
    ]
    return InlineKeyboardMarkup(keyboard)