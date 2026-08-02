from telegram.ext import ApplicationBuilder, CommandHandler, filters, MessageHandler, CallbackQueryHandler
from telegram import Update
from handlers.settings import BOT_TOKEN


def main():
    print("Starting Bot ...")
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", ))
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()