from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

BOT_TOKEN = '7649317053:AAEuahOjsqpu2aqQGs5qlJCsKvL35qU-leo'

async def call_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    members = await context.bot.get_chat_administrators(chat.id)
    mentions = [f"@{m.user.username}" for m in members if m.user.username]
    message = " ".join(mentions) + "\n" + " ".join(context.args)
    await update.message.reply_text(message, parse_mode=ParseMode.HTML)

if __name__ == '__main__':
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler('alo', call_command))
    app.run_polling()
