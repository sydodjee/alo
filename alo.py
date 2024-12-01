from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import os

BOT_TOKEN = '7649317053:AAEuahOjsqpu2aqQGs5qlJCsKvL35qU-leo'
WEBHOOK_URL = f"https://{os.environ.get('RENDER_EXTERNAL_HOSTNAME')}"  # Render автоматически предоставит URL

async def call_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    members = await context.bot.get_chat_members(chat.id)  # Получаем всех участников чата

    mentions = []
    for member in members:
        # Проверяем, что у пользователя есть юзернейм
        if member.user.username:
            mentions.append(f"@{member.user.username}")

    # Если есть участники с юзернеймами, формируем сообщение
    if mentions:
        message = " ".join(mentions) + "\n" + " ".join(context.args)
        await update.message.reply_text(message, parse_mode=ParseMode.MARKDOWN)
    else:
        await update.message.reply_text("Нет участников с юзернеймами!")

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
