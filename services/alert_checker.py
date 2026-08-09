from telegram.ext import Application
from telegram.constants import ParseMode
import logging


async def check_alerts(app: Application):
    alert_repo = app.bot_data["alert_repo"]
    price_service = app.bot_data["price_service"]

    active_alerts = await alert_repo.get_all_active()

    for alert in active_alerts:
        price_data = await price_service.get_price(alert.symbol, alert.vs_currency)
        if price_data is None:
            continue

        current_price = price_data["price"]
        triggered = (
            (alert.direction == "above" and current_price >= alert.target_price) or
            (alert.direction == "below" and current_price <= alert.target_price)
        )

        if triggered:
            direction_text = "بالاتر رفت" if alert.direction == "above" else "پایین‌تر اومد"
            try:
                await app.bot.send_message(
                    chat_id=alert.user_id,
                    text=(
                        f"🔔 هشدار قیمت!\n\n"
                        f"{alert.symbol} از {alert.target_price:,.0f} تومان {direction_text}\n"
                        f"قیمت الان: {current_price:,.0f} تومان"
                    ),
                    parse_mode=ParseMode.HTML
                )
                await alert_repo.deactivate(alert.id)
            except Exception as e:
                logger = logging.getLogger(__name__)
                logger.error(f"Alert Error: {e}")