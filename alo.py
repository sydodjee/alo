from telegram import Update, ParseMode
from telegram.ext import Updater, CommandHandler, CallbackContext

# Function to fetch and tag all members in a group
def tag_all(update: Update, context: CallbackContext) -> None:
    try:
        chat = update.effective_chat
        bot = context.bot
        
        # Fetch all members of the group
        members = bot.get_chat_administrators(chat.id)  # Get admins first
        members += bot.get_chat_members(chat.id)  # Get all members (may be limited)
        
        usernames = []
        for member in members:
            if member.user.username:  # Only include users with usernames
                usernames.append(f"@{member.user.username}")

        if not usernames:
            update.message.reply_text("No usernames found to tag.")
            return

        # Construct the tag message
        tag_message = " ".join(usernames)
        update.message.reply_text(tag_message, parse_mode=ParseMode.MARKDOWN)
    except Exception as e:
        update.message.reply_text(f"Error: {e}")

# Main function to run the bot
def main():
    # Replace 'YOUR_TOKEN_HERE' with your actual bot token
    TOKEN = "YOUR_TOKEN_HERE"
    updater = Updater(TOKEN)

    dp = updater.dispatcher
    dp.add_handler(CommandHandler("tagall", tag_all))

    # Start the bot
    updater.start_polling()
    print("Bot is running...")
    updater.idle()

if __name__ == "__main__":
    main()
