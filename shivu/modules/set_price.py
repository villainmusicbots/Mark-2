from telegram import Update
from telegram.ext import CallbackContext, CommandHandler
from shivu import application, user_collection, OWNER_IDS

# Predefined rarity price ranges
RARITY_PRICE_RANGES = {
    1: (2000, 10000),  # COMMON
    2: (2000, 10000),  # MEDIUM
    3: (2000, 10000),  # RARE
    4: (2000, 10000),  # LEGENDARY
    5: (1000000, 1500000),  # HOT
    6: (1000000, 1500000),  # COLD
    7: (1000000, 1500000),  # LOVE
    8: (1000000, 1500000),  # SCARY
    9: (1000000, 1500000),  # CHRISTMAS
    10: (20000, 40000),  # SPECIAL EDITION
    11: (22000, 44000),  # SHINING
    12: (24000, 48000),  # ANGELIC
    13: (26000, 52000),  # MIX WORLD
    14: (28000, 56000),  # DELUXE EDITION
    15: (30000, 60000),  # MYSTIC
    16: (32000, 64000)   # ROYAL
}

async def set_price(update: Update, context: CallbackContext) -> None:
    user_id = update.effective_user.id
    
    # Check if the user is an authorized owner
    if user_id not in OWNER_IDS:
        await update.message.reply_text("You are not authorized to use this command.")
        return
    
    # Ensure the command is in the correct format
    if len(context.args) != 3:
        await update.message.reply_text("Usage: /setprice <rarity> <min_price> <max_price>")
        return
    
    # Parse the input values
    try:
        rarity = int(context.args[0])
        min_price = int(context.args[1])
        max_price = int(context.args[2])
    except ValueError:
        await update.message.reply_text("Invalid input. Please provide numeric values for rarity, min_price, and max_price.")
        return

    # Validate the rarity number
    if rarity not in RARITY_PRICE_RANGES:
        await update.message.reply_text("Invalid rarity number. Valid values are 1-16.")
        return

    # Validate that the min_price is less than max_price
    if min_price >= max_price:
        await update.message.reply_text("Minimum price should be less than maximum price.")
        return

    # Update the price range for the selected rarity
    RARITY_PRICE_RANGES[rarity] = (min_price, max_price)

    # Save the updated price range in a database (optional, if required)
    # For now, we are just updating the in-memory price range.

    await update.message.reply_text(f"Price for rarity {rarity} has been updated: {min_price} - {max_price} coins.")

# Add the /setprice command handler
application.add_handler(CommandHandler("setprice", set_price, block=False))