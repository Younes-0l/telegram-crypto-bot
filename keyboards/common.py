from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def get_back_button(target: str = "main") -> InlineKeyboardMarkup:
    """
    Specifies which menu the keyboard back button should be directed to.
    """
    keyboard = [
        [InlineKeyboardButton("بازگشت 🔙", callback_data=f"back:{target}")]
    ]
    return InlineKeyboardMarkup(keyboard)