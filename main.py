from telegram.ext import ApplicationBuilder, CommandHandler, filters, MessageHandler, CallbackQueryHandler
from telegram import Update
from handlers.settings import BOT_TOKEN
from handlers import start, price, navigation, watchlist
from database.database import create_tables
from database.redis_client import redis_client
from services.price_service import PriceService
from repositories.watchlist_repository import WatchlistRepository
from repositories.alert_repository import AlertRepository
from services.watchlist_service import WatchlistService
from services.alert_checker import check_alerts
from handlers.alert_conversation import alert_conversation_handler


async def alert_check_job(context):
    await check_alerts(context.application)

create_tables()

def main():
    print("Starting Crypto Bot ...")
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    price_service = PriceService(redis_client=redis_client)
    watchlist_repo = WatchlistRepository()

    watchlist_service = WatchlistService(
        watchlist_repo=watchlist_repo,
        price_service=price_service,
    )

    app.bot_data["alert_repo"] = AlertRepository()


    app.bot_data["redis_client"] = redis_client
    app.bot_data["price_service"] = price_service
    app.bot_data["watchlist_service"] = watchlist_service

    app.add_handler(CommandHandler("start", start.start))

    app.add_handler(CallbackQueryHandler(price.show_price_menu, pattern=r"^menu:price$"))
    app.add_handler(CallbackQueryHandler(price.show_coin_price, pattern=r"^coin:\w+$"))
    
    app.add_handler(CallbackQueryHandler(navigation.go_back, pattern=r"^back:\w+$"))
    app.add_handler(CallbackQueryHandler(watchlist.show_watchlist, pattern=r"^menu:watchlist$"))
    app.add_handler(CallbackQueryHandler(watchlist.start_add_coin, pattern=r"^watchlist_add$"))
    app.add_handler(CallbackQueryHandler(watchlist.confirm_add_coin, pattern=r"^watchlist_add_coin:\w+$"))
    app.add_handler(CallbackQueryHandler(watchlist.remove_coin, pattern=r"^watchlist_remove:\w+$"))

    app.add_handler(alert_conversation_handler)

    app.job_queue.run_repeating(alert_check_job, interval=60, first=10)

    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()