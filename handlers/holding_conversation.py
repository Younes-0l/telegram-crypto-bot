from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler, MessageHandler, filters, CallbackQueryHandler, CommandHandler
from keyboards.coin_menu import get_coin_selection_menu
from .start import start


SELECT_COIN, ENTER_AMOUNT, ENTER_AVG_PRICE = range(3)


async def start_holding(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.message.edit_text(
        "کدوم ارز رو می‌خوای به پورتفولیو اضافه کنی؟",
        reply_markup=get_coin_selection_menu(prefix="holding_coin")
    )
    return SELECT_COIN


async def start_holding_edit(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """"""
    query = update.callback_query
    symbol = query.data.split(":")[1]
    context.user_data["holding_symbol"] = symbol
    context.user_data["is_editing"] = True  # برای تشخیص متن پیام بعدی

    await query.answer()
    await query.message.edit_text(
        f"در حال ویرایش {symbol}\n\nمقدار جدیدت چقدره؟ (مثلاً 0.015)"
    )
    return ENTER_AMOUNT


async def coin_selected(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    symbol = query.data.split(":")[1]
    context.user_data["holding_symbol"] = symbol
    context.user_data["is_editing"] = False

    await query.answer()
    await query.message.edit_text(f"ارز: {symbol}\n\nچقدر {symbol} داری؟ (مثلاً 0.015)")
    return ENTER_AMOUNT


async def amount_entered(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    try:
        amount = float(text)
        if amount <= 0:
            raise ValueError
    except ValueError:
        await update.message.reply_text("لطفاً یک عدد معتبر و مثبت وارد کن: ⚠️")
        return ENTER_AMOUNT

    context.user_data["holding_amount"] = amount

    prompt = (
        "میانگین قیمت خرید جدید رو وارد کن (تومان، هر واحد):"
        if context.user_data.get("is_editing")
        else "میانگین قیمت خریدت چند بوده؟ (تومان، هر واحد)"
    )
    await update.message.reply_text(prompt)
    return ENTER_AVG_PRICE


async def avg_price_entered(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.bot.send_chat_action(update.effective_chat.id, "typing")

    text = update.message.text.strip()
    try:
        avg_price = float(text)
        if avg_price <= 0:
            raise ValueError
    except ValueError:
        await update.message.reply_text("لطفاً یک عدد معتبر و مثبت وارد کن: ⚠️")
        return ENTER_AVG_PRICE

    symbol = context.user_data["holding_symbol"]
    amount = context.user_data["holding_amount"]
    is_editing = context.user_data.get("is_editing", False)
    user_id = update.effective_user.id

    portfolio_service = context.bot_data["portfolio_service"]
    await portfolio_service.set_holding(user_id, symbol, amount, avg_price)

    action_text = "به‌روزرسانی شد" if is_editing else "ثبت شد"
    await update.message.reply_text(f"{action_text}: {amount:g} {symbol} با میانگین خرید {avg_price:,.0f} تومان ✅")

    context.user_data.clear()
    return ConversationHandler.END


async def cancel_holding(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()
    await update.message.reply_text("لغو شد.")
    return ConversationHandler.END

async def cancel_and_restart(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()
    await start(update, context)
    return ConversationHandler.END

holding_conversation_handler = ConversationHandler(
    entry_points=[
        CallbackQueryHandler(start_holding, pattern=r"^holding_add$"),
        CallbackQueryHandler(start_holding_edit, pattern=r"^holding_edit:\w+$"),
        ],
    states={
        SELECT_COIN: [CallbackQueryHandler(coin_selected, pattern=r"^holding_coin:\w+$")],
        ENTER_AMOUNT: [MessageHandler(filters.TEXT & ~filters.COMMAND, amount_entered)],
        ENTER_AVG_PRICE: [MessageHandler(filters.TEXT & ~filters.COMMAND, avg_price_entered)],
    },
    fallbacks=[
        CommandHandler("cancel", cancel_holding),
        CommandHandler("start", cancel_and_restart),
        ],
)