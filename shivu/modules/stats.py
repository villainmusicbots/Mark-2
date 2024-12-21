import logging
from telegram import Update
from telegram.ext import CommandHandler, CallbackContext
from shivu import application
from config import OWNER_IDS  # Assuming OWNER_IDS is imported from config.py

# Logging to track errors
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Dual owners
OWNER_IDS = [5909658683, 8019277081]

async def stats(update: Update, context: CallbackContext) -> None:
    """Command to show stats for owner"""
    user_id = update.effective_user.id

    # Check if the user is an owner
    if user_id not in OWNER_IDS:
        await update.message.reply_text("You are not authorized to use this command.")
        return

    # Example stats
    total_users = 902  # Replace with dynamic count from your data
    total_groups = 154  # Replace with dynamic count from your data

    await update.message.reply_text(f"Total Users: {total_users}\nTotal Groups: {total_groups}")

# Add the command handler for /stats
application.add_handler(CommandHandler("stats", stats))
