from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# === НАСТРОЙКИ ===
TOKEN = "8417773265:AAF6y_yLSCfL94b3is63sK2YRBQP2b2FvfY"
ADMIN_ID = 6580598992


# === /start ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Привет! Отправь сюда сообщение — я передам его администратору *анонимно*.",
        parse_mode="Markdown"
    )

# === /reply — ответ админу пользователю ===
async def reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("⛔ У вас нет прав для этой команды.")
        return

    if len(context.args) < 2:
        await update.message.reply_text("❗ Используй формат: /reply user_id сообщение")
        return

    user_id = context.args[0]
    reply_text = " ".join(context.args[1:])

    try:
        await context.bot.send_message(chat_id=user_id, text=f"💬 Ответ от администратора:\n\n{reply_text}")
        await update.message.reply_text("✅ Ответ отправлен пользователю.")
    except Exception as e:
        await update.message.reply_text(f⚠️ Ошибка при отправке: {e}")

# === Обработка входящих сообщений ===
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    text = update.message.text

    # Получаем информацию об отправителе
    name = user.full_name or "Без имени"
    username = f"@{user.username}" if user.username else "(username отсутствует)"
    user_id = user.id

    # Формируем сообщение админу
    msg = (
        f"📨 Новое анонимное сообщение:\n\n"
        f"{text}\n\n"
        f"👤 Имя: {name}\n"
        f"🔗 Username: {username}\n"
        f"🆔 ID: {user_id}\n\n"
        f"🔁 Чтобы ответить, используй:\n"
        f"/reply {user_id} твой_ответ_сюда"
    )

    # Отправляем админу
    await context.bot.send_message(chat_id=ADMIN_ID, text=msg)

    # Подтверждаем пользователю
    await update.message.reply_text("✅ Сообщение отправлено анонимно!")

# === ЗАПУСК ===
def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("reply", reply))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("🤖 Бот запущен и работает...")
    app.run_polling()

if __name__ == "__main__":
    main()
