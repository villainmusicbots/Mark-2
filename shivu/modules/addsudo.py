import logging
from telegram import Update
from telegram.ext import CommandHandler, CallbackContext
from shivu import application
from shivu import sudo_users
from config import SUDO_USERS, OWNER_ID  # Assuming OWNER_ID and SUDO_USERS are imported from config.py

# Logging to track errors
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def add_sudo(update: Update, context: CallbackContext) -> None:
    """Command to add a new sudo user."""
    user_id = update.effective_user.id

    # Check if the user is the owner or a sudo user
    if user_id not in SUDO_USERS and user_id != OWNER_ID:
        await update.message.reply_text("You do not have permission to add sudo users.")
        return

    # Make sure a user ID is provided
    if not context.args:
        await update.message.reply_text("Please provide the user ID to add as sudo.")
        return

    new_sudo_user_id = context.args[0]

    # Check if the provided user ID is already a sudo user
    if new_sudo_user_id in SUDO_USERS:
        await update.message.reply_text(f"User {new_sudo_user_id} is already a sudo user.")
        return

    # Add the new user to the sudo users list
    SUDO_USERS.append(new_sudo_user_id)

    # Update the config file or wherever sudo users are stored
    try:
        with open("config.py", "a") as config_file:
            config_file.write(f'\nSUDO_USERS = {SUDO_USERS}')
        
        await update.message.reply_text(f"User {new_sudo_user_id} has been added as a sudo user!")
    except Exception as e:
        logger.error(f"Error updating sudo users: {e}")
        await update.message.reply_text("Failed to add the user as sudo. Please try again later.")

# Add the command handler for /addsudo
application.add_handler(CommandHandler("addsudo", add_sudo))