from keyboards.main_menu import get_main_menu
from services.user_service import UserService
from telegram import CallbackQuery, Update
from telegram.ext import ContextTypes
from repositories import user_reepository


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_repo = user_reepository.UserRepository()
    tel_user = update.effective_user
    user_service = UserService(user_repo=user_repo)
    user, is_new = user_service.get_or_create_user(
        telegram_id=tel_user.id,
        full_name=tel_user.full_name,
        username=tel_user.username,
    )

    text = (
        "🚀 به ربات ارز دیجیتال خوش اومدی!\n\n"
        "با این ربات می‌تونی:\n"
        "💰 قیمت لحظه‌ای ارزها رو ببینی\n"
        "⭐ واچ‌لیست شخصی بسازی\n"
        "🔔 هشدار قیمت تنظیم کنی\n"
        "📊 پورتفولیوت رو مدیریت کنی"
    ) if is_new else "🚀 دوباره خوش اومدی!"

    await update.message.reply_text(text=text, reply_markup=get_main_menu())