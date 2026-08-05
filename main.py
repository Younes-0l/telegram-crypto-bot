from telegram.ext import ApplicationBuilder, CommandHandler, filters, MessageHandler, CallbackQueryHandler
from telegram import Update
from handlers.settings import BOT_TOKEN
from handlers import start, price, navigation
from database.database import create_tables
from database.redis_client import redis_client


create_tables()

def main():
    print("Starting Crypto Bot ...")
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.bot_data["redis_client"] = redis_client

    app.add_handler(CommandHandler("start", start.start))
    app.add_handler(CallbackQueryHandler(price.show_price_menu, pattern=r"^menu:price$"))
    app.add_handler(CallbackQueryHandler(price.show_coin_price, pattern=r"^coin:\w+$"))
    app.add_handler(CallbackQueryHandler(navigation.go_back, pattern=r"^back:\w+$"))
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()