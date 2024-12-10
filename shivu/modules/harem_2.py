from telegram import Update
from telegram.ext import CallbackContext
from shivu import user_collection, collection

async def harem(update: Update, context: CallbackContext, page=0) -> None:
    user_id = update.effective_user.id

    # Fetch user's data
    user = await user_collection.find_one({'id': user_id})
    if not user:
        await update.message.reply_text('You Have Not Guessed any Characters Yet..')
        return

    # Get the rarity preference from the user profile
    rarity_preference = user.get('rarity_preference', 'common')

    # Fetch all the characters of the user
    characters = sorted(user['characters'], key=lambda x: (x['anime'], x['id']))

    # Sort characters by rarity preference
    rarity_order = ['common', 'uncommon', 'rare', 'legendary', 'mythical']
    characters_sorted = sorted(characters, key=lambda x: rarity_order.index(x['rarity']) if x['rarity'] else 0)

    # Filter based on the rarity preference
    filtered_characters = [c for c in characters_sorted if c['rarity'] == rarity_preference]

    if not filtered_characters:
        await update.message.reply_text(f"You have no {rarity_preference} characters.")
        return

    # Prepare the message to display the characters in the harem
    harem_message = f"<b>{update.effective_user.first_name}'s Harem (Rarity: {rarity_preference.capitalize()})</b>\n"
    for character in filtered_characters:
        harem_message += f"{character['name']} - {character['rarity']} ({character['id']})\n"

    await update.message.reply_text(harem_message)

# Add the handler for /harem
application.add_handler(CommandHandler("harem", harem, block=False))