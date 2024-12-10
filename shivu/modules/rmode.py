from telegram import Update
from telegram.ext import CommandHandler, CallbackContext
from shivu import user_collection

async def rmode(update: Update, context: CallbackContext) -> None:
    user_id = update.effective_user.id
    rarity = context.args[0].lower() if context.args else None  # Get rarity from user input

    # List of possible rarities to prevent invalid input
    valid_rarities = ['common', 'uncommon', 'rare', 'legendary', 'mythical']

    if rarity not in valid_rarities:
        await update.message.reply_text("Invalid rarity! Please choose from: common, uncommon, rare, legendary, mythical.")
        return

    # Save the rarity setting to the user's profile
    await user_collection.update_one(
        {'id': user_id},
        {'$set': {'rarity_preference': rarity}},
        upsert=True
    )

    await update.message.reply_text(f"Your rarity preference has been set to {rarity.capitalize()}!")

# Add the handler for /rmode
application.add_handler(CommandHandler("rmode", rmode, block=False))