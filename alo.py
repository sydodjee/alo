from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import os

BOT_TOKEN = '7649317053:AAEuahOjsqpu2aqQGs5qlJCsKvL35qU-leo'
WEBHOOK_URL = f"https://{os.environ.get('RENDER_EXTERNAL_HOSTNAME')}"  # Render автоматически предоставит URL

# Функция для добавления пользователя в файл (если он еще не добавлен)
def add_user(username):
    if username is None:
        return
    # Проверяем, если такого пользователя нет в файле
    with open('users.txt', 'r') as f:
        users = f.readlines()
    users = [user.strip() for user in users]

    if username not in users:
        with open('users.txt', 'a') as f:
            f.write(f"{username}\n")

# Функция для получения всех пользователей из файла
def get_all_users():
    if not os.path.exists('users.txt'):
        return []
    
    with open('users.txt', 'r') as f:
        users = f.readlines()
    return [user.strip() for user in users]

# Обработчик всех сообщений (добавляем пользователя в файл)
async def add_user_from_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user.username
    add_user(user)

# Обработчик команды /alo
async def call_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Получаем всех пользователей
    all_users = get_all_users()

    # Создаем строку с упоминаниями всех пользователей
    mentions = [f"@{username}" for username in all_users]
    message = " ".join(mentions) + "\n" + " ".join(context.args)

    # Отправляем сообщение
    await update.message.reply_text(message, parse_mode=ParseMode.HTML)

if __name__ == '__main__':
    # Создаем приложение
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # Обработчик всех сообщений
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, add_user_from_message))

    # Обработчик команды /alo
    app.add_handler(CommandHandler('alo', call_command))

    # Настроим webhook
    app.run_webhook(
        listen="0.0.0.0", 
        port=int(os.environ.get("PORT", 8443)), 
        url_path=BOT_TOKEN,
        webhook_url=f"{WEBHOOK_URL}/{BOT_TOKEN}"
    )
