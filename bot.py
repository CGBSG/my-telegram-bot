from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

def start(update: Update, context: CallbackContext):
    update.message.reply_text('👋 سلام! من ربات شما هستم.')

def echo(update: Update, context: CallbackContext):
    update.message.reply_text(f'شما نوشتید: {update.message.text}')

def main():
    updater = Updater(os.environ["TOKEN"])
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
