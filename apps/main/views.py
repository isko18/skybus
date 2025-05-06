from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import django
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")  # замените на своё
django.setup()

from apps.main.models import Driver

# /start команда
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    button = KeyboardButton("Поделиться номером", request_contact=True)
    markup = ReplyKeyboardMarkup([[button]], resize_keyboard=True, one_time_keyboard=True)

    await update.message.reply_text("Пожалуйста, поделитесь номером телефона:", reply_markup=markup)

# Обработка номера телефона
async def contact_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    contact = update.message.contact
    phone = contact.phone_number.replace("+", "").replace(" ", "")
    tg_id = update.effective_user.id

    # Проверяем наличие номера в базе
    driver = Driver.objects.filter(phone_number__icontains=phone).first()

    if driver:
        driver.telegram_id = tg_id
        driver.save()
        await update.message.reply_text(f"Привет, {driver.full_name_driver}! Вы успешно привязаны к системе.")
    else:
        await update.message.reply_text("Ваш номер не найден в базе.")

# Запуск бота
def main():
    TOKEN = "8071056418:AAEcUcGNKYC8yD3gxRF-buNhwgNYM6HbI5k"  # 🔁 замените на токен вашего бота
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.CONTACT, contact_handler))

    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
