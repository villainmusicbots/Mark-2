import urllib.request
from pymongo import ReturnDocument
from telegram import Update
from telegram.ext import CommandHandler, CallbackContext
from shivu import application, sudo_users, collection, db, CHARA_CHANNEL_ID, SUPPORT_CHAT

# Define the rarity map globally for consistency
RARITY_MAP = {
    1: "⚪ COMMON",
    2: "🟢 MEDIUM",
    3: "🟣 RARE",
    4: "🟡 LEGENDARY",
    5: "🏖️ HOT",
    6: "❄ COLD",
    7: "💞 LOVE",
    8: "🎃 SCARY",
    9: "🎄 CHRISTMAS",
    10: "✨ SPECIAL EDITION",
    11: "💫 SHINING",
    12: "🪽 ANGELIC",
    13: "🧬 MIX WORLD",
    14: "🔮 DELUXE EDITION",
    15: "🥵 MYSTIC",
    16: "👑 ROYAL"
}

WRONG_FORMAT_TEXT = """Wrong ❌ format...  eg. /upload Img_url muzan-kibutsuji Demon-slayer 3

img_url character-name anime-name rarity-number

Use rarity number accordingly to the rarity map:
1: ⚪ COMMON, 2: 🟢 MEDIUM, ..., 16: 👑 ROYAL."""

async def get_next_sequence_number(sequence_name):
    sequence_collection = db.sequences
    sequence_document = await sequence_collection.find_one_and_update(
        {'_id': sequence_name},
        {'$inc': {'sequence_value': 1}},
        return_document=ReturnDocument.AFTER
    )
    if not sequence_document:
        await sequence_collection.insert_one({'_id': sequence_name, 'sequence_value': 0})
        return 0
    return sequence_document['sequence_value']

async def upload(update: Update, context: CallbackContext) -> None:
    if str(update.effective_user.id) not in sudo_users:
        await update.message.reply_text('Ask My Owner...')
        return

    try:
        args = context.args
        if len(args) != 4:
            await update.message.reply_text(WRONG_FORMAT_TEXT)
            return

        character_name = args[1].replace('-', ' ').title()
        anime = args[2].replace('-', ' ').title()

        try:
            urllib.request.urlopen(args[0])
        except:
            await update.message.reply_text('Invalid URL.')
            return

        try:
            rarity = RARITY_MAP[int(args[3])]
        except KeyError:
            await update.message.reply_text('Invalid rarity number. Please use a number between 1 and 16.')
            return

        id = str(await get_next_sequence_number('character_id')).zfill(2)

        character = {
            'img_url': args[0],
            'name': character_name,
            'anime': anime,
            'rarity': rarity,
            'id': id
        }

        try:
            message = await context.bot.send_photo(
                chat_id=CHARA_CHANNEL_ID,
                photo=args[0],
                caption=f'<b>Character Name:</b> {character_name}\n<b>Anime Name:</b> {anime}\n<b>Rarity:</b> {rarity}\n<b>ID:</b> {id}\nAdded by <a href="tg://user?id={update.effective_user.id}">{update.effective_user.first_name}</a>',
                parse_mode='HTML'
            )
            character['message_id'] = message.message_id
            await collection.insert_one(character)
            await update.message.reply_text('Character added successfully.')
        except:
            await collection.insert_one(character)
            await update.message.reply_text("Character added to database but not posted to the channel.")
    except Exception as e:
        await update.message.reply_text(f'Upload failed. Error: {str(e)}')

async def delete(update: Update, context: CallbackContext) -> None:
    if str(update.effective_user.id) not in sudo_users:
        await update.message.reply_text('Ask My Owner...')
        return

    try:
        args = context.args
        if len(args) != 1:
            await update.message.reply_text('Incorrect format. Use: /delete ID')
            return

        character = await collection.find_one_and_delete({'id': args[0]})

        if character:
            try:
                await context.bot.delete_message(chat_id=CHARA_CHANNEL_ID, message_id=character['message_id'])
                await update.message.reply_text('Character deleted successfully.')
            except:
                await update.message.reply_text('Character deleted from the database but not found in the channel.')
        else:
            await update.message.reply_text('Character ID not found.')
    except Exception as e:
        await update.message.reply_text(f'Deletion failed. Error: {str(e)}')

async def update(update: Update, context: CallbackContext) -> None:
    if str(update.effective_user.id) not in sudo_users:
        await update.message.reply_text('Ask My Owner...')
        return

    try:
        args = context.args
        if len(args) != 3:
            await update.message.reply_text('Incorrect format. Use: /update ID field new_value')
            return

        character = await collection.find_one({'id': args[0]})
        if not character:
            await update.message.reply_text('Character ID not found.')
            return

        valid_fields = ['img_url', 'name', 'anime', 'rarity']
        if args[1] not in valid_fields:
            await update.message.reply_text(f'Invalid field. Use one of: {", ".join(valid_fields)}.')
            return

        new_value = args[2]
        if args[1] in ['name', 'anime']:
            new_value = new_value.replace('-', ' ').title()
        elif args[1] == 'rarity':
            try:
                new_value = RARITY_MAP[int(new_value)]
            except KeyError:
                await update.message.reply_text('Invalid rarity number. Use a number between 1 and 16.')
                return

        await collection.find_one_and_update({'id': args[0]}, {'$set': {args[1]: new_value}})

        if args[1] == 'img_url':
            await context.bot.delete_message(chat_id=CHARA_CHANNEL_ID, message_id=character['message_id'])
            message = await context.bot.send_photo(
                chat_id=CHARA_CHANNEL_ID,
                photo=new_value,
                caption=f'<b>Character Name:</b> {character["name"]}\n<b>Anime Name:</b> {character["anime"]}\n<b>Rarity:</b> {character["rarity"]}\n<b>ID:</b> {character["id"]}\nUpdated by <a href="tg://user?id={update.effective_user.id}">{update.effective_user.first_name}</a>',
                parse_mode='HTML'
            )
            await collection.find_one_and_update({'id': args[0]}, {'$set': {'message_id': message.message_id}})
        else:
            await context.bot.edit_message_caption(
                chat_id=CHARA_CHANNEL_ID,
                message_id=character['message_id'],
                caption=f'<b>Character Name:</b> {character["name"]}\n<b>Anime Name:</b> {character["anime"]}\n<b>Rarity:</b> {new_value}\n<b>ID:</b> {character["id"]}\nUpdated by <a href="tg://user?id={update.effective_user.id}">{update.effective_user.first_name}</a>',
                parse_mode='HTML'
            )

        await update.message.reply_text('Character updated successfully.')
    except Exception as e:
        await update.message.reply_text(f'Update failed. Error: {str(e)}')

# Handlers
UPLOAD_HANDLER = CommandHandler('upload', upload, block=False)
DELETE_HANDLER = CommandHandler('delete', delete, block=False)
UPDATE_HANDLER = CommandHandler('update', update, block=False)

# Add handlers to the application
application.add_handler(UPLOAD_HANDLER)
application.add_handler(DELETE_HANDLER)
application.add_handler(UPDATE_HANDLER)
