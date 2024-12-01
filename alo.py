from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import os

BOT_TOKEN = '7649317053:AAEuahOjsqpu2aqQGs5qlJCsKvL35qU-leo'
WEBHOOK_URL = f"https://{os.environ.get('RENDER_EXTERNAL_HOSTNAME')}"

async def call_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    mentions = []

    try:
        # Получаем всех участников чата
        members = await context.bot.get_chat_administrators(chat.id)

        # Генерируем список псевдонимов (символов), чтобы упомянуть всех участников
        for i, member in enumerate(members):
            mentions.append(f"User_{i+1}")

        if mentions:
            message = " ".join(mentions) + "\n" + " ".join(context.args)
        else:
            message = "Не удалось найти активных участников."

        await update.message.reply_text(message, parse_mode=ParseMode.HTML)

    except Exception as e:
        await update.message.reply_text(
            f"Ошибка: {e}",
            parse_mode=ParseMode.HTML
        )

if __name__ == '__main__':
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler('alo', call_command))

    # Настраиваем webhook
    app.run_webhook(
        listen="0.0.0.0", 
        port=int(os.environ.get("PORT", 8443)), 
        url_path=BOT_TOKEN,
        webhook_url=f"{WEBHOOK_URL}/{BOT_TOKEN}"
    )
