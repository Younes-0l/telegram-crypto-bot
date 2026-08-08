from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def get_direction_menu():
    keyboard = [
        [InlineKeyboardButton("📈 بالاتر رفت", callback_data="alert_direction:above")],
        [InlineKeyboardButton("📉 پایین‌تر اومد", callback_data="alert_direction:below")],
    ]
    return InlineKeyboardMarkup(keyboard)