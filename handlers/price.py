from telegram import Update, CallbackQuery
from telegram.ext import ContextTypes
from services.price_service import PriceService
from keyboards.coin_menu import get_coin_selection_menu
from services.helpers import format_number
from keyboards.common import get_back_button


async def show_price_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.message.edit_text(
        "ارز موردنظرت رو انتخاب کن:",
        reply_markup=get_coin_selection_menu()
    )
    await query.answer()

async def show_coin_price(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    symbol = str(query.data.split(":")[1])

    redis_client = context.bot_data["redis_client"]
    price_service = PriceService(redis_client=redis_client)

    await query.answer("در حال دریافت قیمت...")
    result = await price_service.get_price(symbol=symbol)
    price = result['price'] if result else None

    if price is None:
        await query.message.edit_text(
            "⚠️ الان نمی‌تونم قیمت رو دریافت کنم، چند لحظه دیگه امتحان کن.",
            reply_markup=get_back_button("price_menu")
        )
        return

    formatted_price = format_number(price)
    await query.message.edit_text(
        f"💰 قیمت {symbol.upper()}: {formatted_price} تومان",
        reply_markup=get_back_button("price_menu")
    )