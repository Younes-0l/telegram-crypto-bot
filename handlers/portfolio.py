from telegram import Update
from telegram.ext import ContextTypes
from keyboards.portfolio_menu import get_portfolio_menu, get_empty_portfolio_menu


async def show_portfolio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id
    portfolio_service = context.bot_data["portfolio_service"]

    await query.answer()
    summary = await portfolio_service.get_portfolio_summary(user_id)

    if not summary:
        await query.message.edit_text(
            "هنوز دارایی‌ای ثبت نکردی.",
            reply_markup=get_empty_portfolio_menu()
        )
        return

    lines = ["📊 پورتفولیو شما:\n"]
    total_profit = 0

    for entry in summary:
        profit_emoji = "🟢" if entry.get("profit", 0) >= 0 else "🔴"
        lines.append(f"{profit_emoji} {entry['symbol']}: {entry['amount']:g} واحد")
        lines.append(f"   میانگین خرید: {entry['avg_buy_price']:,.0f} تومان")

        if entry.get("current_price") is not None:
            lines.append(f"   قیمت الان: {entry['current_price']:,.0f} تومان")
            lines.append(f"   سود/زیان: {entry['profit']:,.0f} تومان ({entry['profit_percent']:+.1f}٪)\n")
            total_profit += entry["profit"]
        else:
            lines.append("   ⚠️ قیمت لحظه‌ای در دسترس نیست\n")

    lines.append(f"💰 مجموع سود/زیان: {total_profit:,.0f} تومان")

    await query.message.edit_text("\n".join(lines), reply_markup=get_portfolio_menu(summary))


async def remove_holding(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    symbol = query.data.split(":")[1]
    user_id = query.from_user.id
    portfolio_service = context.bot_data["portfolio_service"]

    await portfolio_service.remove_holding(user_id, symbol)
    await query.answer(f"🗑 {symbol} حذف شد")

    await show_portfolio(update, context)