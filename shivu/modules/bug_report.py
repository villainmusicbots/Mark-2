from telegram import Update
from telegram.ext import CommandHandler, MessageHandler, Filters, CallbackContext

# Admin ID (Your admin user ID)
ADMIN_USER_ID = 8019277081  # Replace with your actual admin ID

# Start command
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Hello! Use /bug to report any issue.")

# Bug command to initiate bug reporting
def bug(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Please describe the bug or issue you encountered:")

# Handling the bug description
def handle_bug_description(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    bug_description = update.message.text

    # Send the bug description to the admin
    context.bot.send_message(chat_id=ADMIN_USER_ID, text=f"New Bug Report from User ID {user_id}:\n{bug_description}")
    
    update.message.reply_text("Thank you for your report! We will look into it.")

# Register handlers
def register_handlers(dispatcher):
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("bug", bug))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_bug_description))
