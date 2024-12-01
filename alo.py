from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import os

BOT_TOKEN = '7649317053:AAEuahOjsqpu2aqQGs5qlJCsKvL35qU-leo'
WEBHOOK_URL = f"https://{os.environ.get('RENDER_EXTERNAL_HOSTNAME')}"  # Render автоматически предоставит URL

async def call_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    mentions = []

    # Попытка получить всех участников чата
    try:
        # Telegram API не позволяет напрямую получать всех участников в больших группах,
        # поэтому используется перебор ID в диапазоне. Бот должен быть админом.
        members_count = await context.bot.get_chat_member_count(chat.id)

        for user_id in range(1, members_count + 1):
            try:
                member = await context.bot.get_chat_member(chat.id, user_id)
                if member.user.username:  # Упоминаем только пользователей с username
                    mentions.append(f"@{member.user.username}")
                else:  # Если нет username, упоминаем по имени
                    mentions.append(f"<a href='tg://user?id={member.user.id}'>{member.user.first_name}</a>")
            except Exception:
                pass  # Игнорируем ошибки, например, если пользователь недоступен

    except Exception:
        # Если не удалось получить всех участников, выводим сообщение об ошибке
        mentions.append("Не удалось получить список участников. Убедитесь, что бот является администратором.")

    # Формируем сообщение с упоминанием всех
    message = " ".join(mentions) + "\n" + " ".join(context.args)
    await update.message.reply_text(message, parse_mode=ParseMode.HTML)

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
