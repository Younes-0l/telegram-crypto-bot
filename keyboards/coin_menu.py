from telegram import InlineKeyboardMarkup, InlineKeyboardButton

def get_coin_selection_menu(prefix: str = "coin") -> InlineKeyboardMarkup:
    coins = [
        ("BTC", "بیت کوین"), ("ETH", "اتریوم"), ("SOL", "سولانا"), ("USDT", "تتر"),
        ("TON", "تون کوین"), ("NOT", "نات کوین"), ("ADA", "کاردانو"), ("TRX", "ترون"),
    ]
    keyboard = []
    for i in range(0, len(coins), 2):
        row = []
        for symbol, name in coins[i:i+2]:
            row.append(InlineKeyboardButton(f"{symbol} - {name}", callback_data=f"{prefix}:{symbol}"))
        keyboard.append(row)
    keyboard.append([InlineKeyboardButton("بازگشت 🔙", callback_data="back:main")])
    return InlineKeyboardMarkup(keyboard)