from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def get_direction_menu():
    keyboard = [
        [InlineKeyboardButton("بالاتر رفت 📈", callback_data="alert_direction:above")],
        [InlineKeyboardButton("پایین‌تر اومد 📉", callback_data="alert_direction:below")],
    ]
    return InlineKeyboardMarkup(keyboard)

def get_alerts_list_menu(alerts: list) -> InlineKeyboardMarkup:
    keyboard = []

    for alert in alerts:
        direction_emoji = "📈" if alert.direction == "above" else "📉"
        label = f"{direction_emoji} {alert.symbol}: {alert.target_price:,.0f} تومان"
        row = [
            InlineKeyboardButton(label, callback_data="noop"),
            InlineKeyboardButton("❌", callback_data=f"alert_remove:{alert.id}"),
        ]
        keyboard.append(row)

    keyboard.append([InlineKeyboardButton("افزودن هشدار ➕", callback_data="alert_add")])
    keyboard.append([InlineKeyboardButton("بازگشت 🔙", callback_data="back:main")])

    return InlineKeyboardMarkup(keyboard)


def get_empty_alerts_menu() -> InlineKeyboardMarkup:
    keyboard = [
        [InlineKeyboardButton("افزودن هشدار ➕", callback_data="alert_add")],
        [InlineKeyboardButton("بازگشت 🔙", callback_data="back:main")],
    ]
    return InlineKeyboardMarkup(keyboard)