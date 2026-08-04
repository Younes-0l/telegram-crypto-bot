from telegram import InlineKeyboardMarkup, InlineKeyboardButton


def get_coin_selection_menu():
    keyboard = [
        [InlineKeyboardButton("BTC - بیت کوین", callback_data="coin:BTC"), InlineKeyboardButton("ETH - اتریوم", callback_data="coin:ETH")],
        [InlineKeyboardButton("SOL - سولانا", callback_data="coin:SOL"), InlineKeyboardButton("USDT - تتر", callback_data="coin:USDT")],
        [InlineKeyboardButton("TON - تون کوین", callback_data="coin:TON"), InlineKeyboardButton("NOT - نات کوین", callback_data="coin:NOT")],
        [InlineKeyboardButton("ADA - کاردانو", callback_data="coin:ADA"), InlineKeyboardButton("TRX - ترون", callback_data="coin:TRX")],
        [InlineKeyboardButton("بازگشت 🔙", callback_data=f"back:main")]

    ]
    return InlineKeyboardMarkup(keyboard)