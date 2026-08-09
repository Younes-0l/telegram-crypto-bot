from telegram import Update
from telegram.ext import ContextTypes
from keyboards.watchlist_menu import get_watchlist_menu, get_empty_watchlist_menu
from keyboards.coin_menu import get_coin_selection_menu


async def show_watchlist(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id
    watchlist_service = context.bot_data["watchlist_service"]

    await query.answer()
    entries = await watchlist_service.get_watchlist_with_prices(user_id)

    if not entries:
        await query.message.edit_text(
            "لیست واچ‌لیستت خالیه. یه ارز اضافه کن تا اینجا ببینیش.",
            reply_markup=get_empty_watchlist_menu()
        )
        return

    text = "واچ‌لیست شما: ⭐\n\nبرای حذف یک ارز، روی ❌ کنارش بزن."
    await query.message.edit_text(text, reply_markup=get_watchlist_menu(entries))


async def start_add_coin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.message.edit_text(
        "کدوم ارز رو می‌خوای به واچ‌لیست اضافه کنی؟",
        reply_markup=get_coin_selection_menu(prefix="watchlist_add_coin")
    )


async def confirm_add_coin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    symbol = query.data.split(":")[1]
    user_id = query.from_user.id
    watchlist_service = context.bot_data["watchlist_service"]

    added = await watchlist_service.add_coin(user_id, symbol)

    if added:
        await query.answer(f"{symbol} به واچ‌لیست اضافه شد ✅")
    else:
        await query.answer(f"{symbol} از قبل توی لیستت هست ⚠️", show_alert=True)

    await show_watchlist(update, context)


async def remove_coin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    symbol = query.data.split(":")[1]
    user_id = query.from_user.id
    watchlist_service = context.bot_data["watchlist_service"]

    await watchlist_service.remove_coin(user_id, symbol)
    await query.answer(f"{symbol} حذف شد 🗑")

    await show_watchlist(update, context)