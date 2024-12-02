from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import Updater, CommandHandler, CallbackContext

# Function to handle the /start command
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(
        "Hello! I am your tagging bot.\n"
        "Use /tagall to mention all members with usernames in this group."
    )

# Function to tag all users with usernames
def tag_all(update: Update, context: CallbackContext) -> None:
    try:
        chat = update.effective_chat
        bot = context.bot

        # Get all members of the group (admins and other members with usernames)
        admins = bot.get_chat_administrators(chat.id)
        usernames = [f"@{admin.user.username}" for admin in admins if admin.user.username]

        # Respond with tagged usernames
        if not usernames:
            update.message.reply_text("No usernames found to tag.")
            return

        tag_message = " ".join(usernames)
        update.message.reply_text(tag_message, parse_mode=ParseMode.MARKDOWN)
    except Exception as e:
        update.message.reply_text(f"An error occurred: {e}")

# Main function to run the bot
def main():
    # Replace 'YOUR_TOKEN_HERE' with your bot token
    TOKEN = "7649317053:AAEuahOjsqpu2aqQGs5qlJCsKvL35qU-leo"
    updater = Updater(TOKEN)

    # Add command handlers
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("tagall", tag_all))

    # Start the bot
    updater.start_polling()
    print("Bot is running...")
    updater.idle()

if __name__ == "__main__":
    main()
