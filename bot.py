import os
import random
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# حالت‌های بازی
GAME_STATES = {}

# لیست حروف فارسی (حروف سخت حذف شده‌اند)
PERSIAN_LETTERS = [
    'آ', 'ا', 'ب', 'پ', 'ت', 'ث', 'ج', 'چ', 'ح', 'خ', 'د', 'ذ', 'ر', 'ز', 'ژ', 'س',
    'ش', 'ص', 'ض', 'ط', 'ظ', 'ع', 'غ', 'ف', 'ق', 'ک', 'گ', 'ل', 'م', 'ن', 'و', 'ه', 'ی'
]

# دسته‌بندی‌های بازی
CATEGORIES = {
    'اسم': '👤 نام',
    'فامیل': '🏠 فامیل',
    'شهر': '🏙 شهر',
    'کشور': '🌍 کشور',
    'حیوان': '🐯 حیوان',
    'غذا': '🍔 غذا'
}

def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        "🎮 به ربات بازی اسم فامیل خوش آمدید!\n"
        "برای شروع بازی از دستور /new_game استفاده کنید."
    )

def new_game(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    letter = random.choice(PERSIAN_LETTERS)
    
    GAME_STATES[user_id] = {
        'letter': letter,
        'answers': {},
        'score': 0
    }

    # ایجاد تایمر ۲ دقیقه‌ای
    context.job_queue.run_once(end_game, 120, context=user_id, name=str(user_id))

    update.message.reply_text(
        f"🎲 بازی جدید شروع شد!\n"
        f"📝 حرف انتخاب شده: {letter}\n"
        f"⏳ زمان شما ۲ دقیقه است!\n\n"
        f"💡 نمونه فرمت پاسخ:\n"
        f"اسم: احمد\n"
        f"فامیل: اکبری\n"
        f"شهر: اصفهان\n"
        f"... (برای هر دسته یک خط)"
    )

def validate_answer(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    if user_id not in GAME_STATES:
        return

    game_data = GAME_STATES[user_id]
    letter = game_data['letter']
    answers = update.message.text.split('\n')
    valid_answers = 0

    for answer in answers:
        try:
            category, value = answer.split(':', 1)
            category = category.strip()
            value = value.strip()

            if category in CATEGORIES and value.startswith(letter):
                game_data['answers'][category] = value
                valid_answers += 1
        except:
            pass

    game_data['score'] += valid_answers
    update.message.reply_text(f"✅ {valid_answers} پاسخ معتبر ثبت شد!")

def end_game(context: CallbackContext):
    user_id = context.job.context
    if user_id not in GAME_STATES:
        return

    game_data = GAME_STATES.pop(user_id)
    results = ["📊 نتایج نهایی:"]

    for cat, ans in game_data['answers'].items():
        results.append(f"{CATEGORIES[cat]}: {ans}")

    results.append(f"\n🏆 امتیاز نهایی: {game_data['score']}")
    context.bot.send_message(user_id, '\n'.join(results))

def help_command(update: Update, context: CallbackContext):
    update.message.reply_text(
        "📚 راهنما:\n"
        "/new_game - شروع بازی جدید\n"
        "در طول بازی پاسخ‌ها را به این فرمت ارسال کنید:\n"
        "اسم: [پاسخ]\nفامیل: [پاسخ]\n..."
    )

def main():
    TOKEN = os.environ.get("TOKEN")
    updater = Updater(TOKEN)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("new_game", new_game))
    dp.add_handler(CommandHandler("help", help_command))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, validate_answer))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
