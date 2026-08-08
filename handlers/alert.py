from telegram import Update
from telegram.ext import ContextTypes
from keyboards.alert_menu import get_alerts_list_menu, get_empty_alerts_menu


async def show_alerts(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id
    alert_repo = context.bot_data["alert_repo"]

    await query.answer()
    alerts = await alert_repo.get_active_for_user(user_id)

    if not alerts:
        await query.message.edit_text(
            "هیچ هشداری تنظیم نکردی. یه هشدار جدید بساز تا اینجا ببینیش.",
            reply_markup=get_empty_alerts_menu()
        )
        return

    text = "🔔 هشدارهای فعال شما:\n\nبرای حذف یک هشدار، روی ❌ کنارش بزن."
    await query.message.edit_text(text, reply_markup=get_alerts_list_menu(alerts))


async def remove_alert(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    alert_id = int(query.data.split(":")[1])
    user_id = query.from_user.id
    alert_repo = context.bot_data["alert_repo"]

    await alert_repo.delete(alert_id, user_id)
    await query.answer("🗑 هشدار حذف شد")

    await show_alerts(update, context)