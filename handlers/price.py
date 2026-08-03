from telegram import Update, CallbackQuery
from telegram.ext import ContextTypes
from services.price_service import PriceService

async def show_coin_price(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    symbol = str(query.data.split(":")[1])
    price_service = PriceService()

    await query.answer("در حال دریافت قیمت...")
    context = await price_service.get_price(symbol=symbol)
    price = context['price']

    if price is None:
        await query.message.edit_text(
            "⚠️ الان نمی‌تونم قیمت رو دریافت کنم، چند لحظه دیگه امتحان کن.",
            # get_back_button
        )
        return

    await query.message.edit_text(
        f"💰 قیمت {symbol.upper()}: {price:,.2f} تومان",
        # get_back_button
    )