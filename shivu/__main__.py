import importlib
import random
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CommandHandler, CallbackContext, MessageHandler, filters

from shivu import application, LOGGER
from shivu.modules import ALL_MODULES

# Load all modules
for module_name in ALL_MODULES:
    importlib.import_module("shivu.modules." + module_name)

async def message_counter(update: Update, context: CallbackContext) -> None:
    # Respond to every message
    await update.message.reply_text(f"{update.effective_user.first_name} Bhai aise hi karte reh 😄")

async def send_image(update: Update, context: CallbackContext) -> None:
    # Example image sending logic (optional)
    await update.message.reply_text("Image sending logic can go here.")

async def guess(update: Update, context: CallbackContext) -> None:
    # Placeholder for guess logic
    await update.message.reply_text("Guess logic can go here.")

async def fav(update: Update, context: CallbackContext) -> None:
    # Placeholder for favorite character logic
    await update.message.reply_text("Favorite character logic can go here.")

def main() -> None:
    """Run bot."""
    application.add_handler(MessageHandler(filters.ALL, message_counter, block=False))
    application.add_handler(CommandHandler(["guess", "protecc", "collect", "grab", "hunt"], guess, block=False))
    application.add_handler(CommandHandler("fav", fav, block=False))

    application.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    LOGGER.info("Bot started")
    main()
