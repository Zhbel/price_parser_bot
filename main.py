from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters
from handlers import message_handler as mh
from handlers import price_handler as ph


async def message_handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_message.entities[0].type != 'bot_command':
        res = mh.MessageHandler(update.effective_message.text)

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=res.message
    )


async def price_handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    document = await context.bot.get_file(update.message.document)
    res = await ph.FileHandler.init(update.message, document)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=res
    )


if __name__ == '__main__':
    token = ""
    application = ApplicationBuilder().token(token).build()

    message_handler = MessageHandler(filters.TEXT, message_handle)
    price_handler = MessageHandler(filters.ATTACHMENT, price_handle)

    application.add_handler(message_handler)
    application.add_handler(price_handler)

    application.run_polling()

