import os
import requests
from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# Токен и репозиторий на GitHub
BOT_TOKEN = '7649317053:AAEuahOjsqpu2aqQGs5qlJCsKvL35qU-leo'
WEBHOOK_URL = f"https://{os.environ.get('RENDER_EXTERNAL_HOSTNAME')}"  # Render автоматически предоставит URL
GITHUB_TOKEN = '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'  # Токен GitHub
GITHUB_REPO = 'sydodjee/bot-users'  # Репозиторий GitHub
GITHUB_FILE_PATH = 'users.txt'  # Путь к файлу в репозитории

# URL для API запросов GitHub
GITHUB_API_URL = f"https://api.github.com/repos/{GITHUB_REPO}/contents/{GITHUB_FILE_PATH}"

# Функция для добавления пользователя в файл на GitHub
def add_user(username):
    if username is None:
        return

    # Получаем текущий контент файла из репозитория
    headers = {'Authorization': f'token {GITHUB_TOKEN}'}
    response = requests.get(GITHUB_API_URL, headers=headers)
    
    if response.status_code == 200:
        file_content = response.json()
        content = file_content['content']
        sha = file_content['sha']  # Получаем sha
        users = requests.utils.unquote(content).splitlines()
    else:
        users = []
        sha = None  # Инициализируем sha как None, если файл не найден

    # Если пользователя еще нет в файле, добавляем его
    if username not in users:
        users.append(username)

    # Кодируем содержимое файла и отправляем обновление в репозиторий
    new_content = "\n".join(users).encode('utf-8')
    encoded_content = requests.utils.quote(new_content)

    # Если sha не найден, то создаем новый файл, иначе обновляем существующий
    if sha:
        # Обновляем файл на GitHub
        update_data = {
            "message": "Add user",
            "sha": sha,
            "content": encoded_content,
        }
        response = requests.put(GITHUB_API_URL, json=update_data, headers=headers)
    else:
        # Создаем новый файл на GitHub, если sha не найден
        update_data = {
            "message": "Create users file",
            "content": encoded_content,
        }
        response = requests.put(GITHUB_API_URL, json=update_data, headers=headers)

    return response.status_code == 200

# Функция для получения всех пользователей из файла на GitHub
def get_all_users():
    headers = {'Authorization': f'token {GITHUB_TOKEN}'}
    response = requests.get(GITHUB_API_URL, headers=headers)

    if response.status_code == 200:
        file_content = response.json()
        content = file_content['content']
        users = requests.utils.unquote(content).splitlines()
        return users
    else:
        return []

# Обработчик всех сообщений (добавляем пользователя в файл на GitHub)
async def add_user_from_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user.username
    if add_user(user):
        print(f"User {user} added to GitHub.")
    else:
        print(f"Failed to add user {user}.")

# Обработчик команды /alo
async def call_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Получаем всех пользователей
    all_users = get_all_users()

    # Проверяем, если список пользователей пустой, не отправляем сообщение
    if not all_users:
        await update.message.reply_text("No users found!")
        return

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
