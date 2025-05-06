from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
)
from apps.main.models import Driver, People
from asgiref.sync import sync_to_async

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    button = KeyboardButton("Поделиться номером", request_contact=True)
    markup = ReplyKeyboardMarkup([[button]], one_time_keyboard=True)
    await update.message.reply_text("Пожалуйста, поделитесь номером телефона:", reply_markup=markup)

# ORM-функции
@sync_to_async
def get_driver_by_phone(phone):
    return Driver.objects.filter(phone_number__icontains=phone).first()

@sync_to_async
def get_driver_by_telegram(tg_id):
    return Driver.objects.filter(telegram_id=tg_id).first()

@sync_to_async
def get_passengers(driver):
    return list(People.objects.filter(driver=driver))

@sync_to_async
def create_placeholder_passenger(tg_id):
    driver = Driver.objects.filter(telegram_id=tg_id).first()
    if not driver:
        return None

    if People.objects.filter(driver=driver).count() >= driver.count:
        return "limit"

    return People.objects.create(
        driver=driver,
        full_name="..................",
        phone=".................."
    )

# Обработка контакта
async def contact_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    contact = update.message.contact
    phone = contact.phone_number.replace("+", "").replace(" ", "")
    tg_id = update.effective_user.id

    driver = await get_driver_by_phone(phone)
    if driver:
        driver.telegram_id = tg_id
        await sync_to_async(driver.save)()

        markup = ReplyKeyboardMarkup([
            ["📋 Список пассажиров", "➕ Добавить пассажира"]
        ], resize_keyboard=True)

        await update.message.reply_text(
            f"Привет, {driver.full_name_driver}! Вы успешно авторизованы.",
            reply_markup=markup
        )
    else:
        await update.message.reply_text("Ваш номер не найден в базе.")

# Обработка кнопки "Список пассажиров"
async def show_passengers(update: Update, context: ContextTypes.DEFAULT_TYPE):
    tg_id = update.effective_user.id
    driver = await get_driver_by_telegram(tg_id)
    if not driver:
        await update.message.reply_text("Вы не авторизованы.\nНажмите на /start для авторизации !")
        return

    passengers = await get_passengers(driver)
    if not passengers:
        await update.message.reply_text("У вас пока нет пассажиров.")
        return

    msg = "\n".join([f"{i+1}. {p.full_name} — {p.phone}" for i, p in enumerate(passengers)])
    await update.message.reply_text(f"Ваши пассажиры:\n{msg}")

# Обработка кнопки "➕ Добавить пассажира"
async def send_input_template(update: Update, context: ContextTypes.DEFAULT_TYPE):
    tg_id = update.effective_user.id
    result = await create_placeholder_passenger(tg_id)

    if result == "limit":
        await update.message.reply_text("❌ Достигнуто максимальное число пассажиров.")
    elif result:
        await update.message.reply_text("✅ Пассажир добавлен.")
    else:
        await update.message.reply_text("❌ Ошибка: вы не авторизованы как водитель.\nНажмите на /start для авторизации !")

# Настройка бота
def create_bot_app():
    TOKEN = "8071056418:AAEcUcGNKYC8yD3gxRF-buNhwgNYM6HbI5k"  # Замените на ваш токен

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.CONTACT, contact_handler))
    app.add_handler(MessageHandler(filters.TEXT & filters.Regex("📋 Список пассажиров"), show_passengers))
    app.add_handler(MessageHandler(filters.TEXT & filters.Regex("➕ Добавить пассажира"), send_input_template))

    return app
