from telegram import Update, ReplyKeyboardRemove
from telegram.ext import ContextTypes, ConversationHandler, MessageHandler, filters, CallbackQueryHandler, CommandHandler
from keyboards.coin_menu import get_coin_selection_menu
from keyboards.alert_menu import get_direction_menu


SELECT_COIN, ENTER_PRICE, SELECT_DIRECTION = range(3)

async def start_alert_creation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.message.edit_text(
        "کدوم ارز رو می‌خوای براش هشدار بذاری؟",
        reply_markup=get_coin_selection_menu(prefix="alert_coin")
    )
    return SELECT_COIN


async def coin_selected(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    symbol = query.data.split(":")[1]
    context.user_data["alert_symbol"] = symbol

    await query.answer()
    await query.message.edit_text(
        f"ارز انتخابی: {symbol}\n\nحالا قیمت هدف رو به تومان وارد کن (فقط عدد):"
    )
    return ENTER_PRICE


async def price_entered(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()

    try:
        target_price = float(text)
        if target_price <= 0:
            raise ValueError
    except ValueError:
        await update.message.reply_text("⚠️ لطفاً فقط یک عدد معتبر و مثبت وارد کن:")
        return ENTER_PRICE

    context.user_data["alert_price"] = target_price

    await update.message.reply_text(
        "وقتی قیمت به این عدد رسید، بالاتر بره خبرت کنم یا پایین‌تر بیاد؟",
        reply_markup=get_direction_menu()
    )
    return SELECT_DIRECTION


async def direction_selected(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    direction = query.data.split(":")[1]

    symbol = context.user_data["alert_symbol"]
    target_price = context.user_data["alert_price"]
    user_id = query.from_user.id

    alert_repo = context.bot_data["alert_repo"]
    await alert_repo.create(user_id, symbol, "IRT", target_price, direction)

    direction_text = "بالاتر رفت" if direction == "above" else "پایین‌تر اومد"
    await query.answer()
    await query.message.edit_text(
        f"✅ هشدار تنظیم شد!\nوقتی {symbol} از {target_price:,.0f} تومان {direction_text}، بهت خبر می‌دم."
    )

    context.user_data.clear()
    return ConversationHandler.END


async def cancel_alert_creation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()
    await update.message.reply_text("لغو شد.", reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END

alert_conversation_handler = ConversationHandler(
    entry_points=[CallbackQueryHandler(start_alert_creation, pattern=r"^alert_add$")],
    states={
        SELECT_COIN: [CallbackQueryHandler(coin_selected, pattern=r"^alert_coin:\w+$")],
        ENTER_PRICE: [MessageHandler(filters.TEXT & ~filters.COMMAND, price_entered)],
        SELECT_DIRECTION: [CallbackQueryHandler(direction_selected, pattern=r"^alert_direction:\w+$")],
    },
    fallbacks=[CommandHandler("cancel", cancel_alert_creation)],
)