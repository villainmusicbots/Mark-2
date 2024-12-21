from config import BOT_TOKEN
import telebot

# Initialize the bot with token from config.py
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['find'])
def find_character(message):
    characters_db = {
        'albedo': {'rarity': 'legendary', 'element': 'geo', 'ids': [1189, 1188, 1187]},
        'goku': {'rarity': 'legendary', 'element': 'fire', 'ids': [1001, 1002, 1003]},
        'hinata': {'rarity': 'rare', 'element': 'earth', 'ids': [2001, 2002, 2003]},
    }

    command_parts = message.text.split(' ', 2)
    if len(command_parts) < 2:
        bot.reply_to(message, "Please provide a character name.")
        return

    character_name = command_parts[1].strip().lower()
    rarity = command_parts[2].strip().lower() if len(command_parts) > 2 else None

    matching_characters = [char for char in characters_db if character_name in char.lower()]

    if matching_characters:
        for character in matching_characters:
            character_data = characters_db[character]
            if rarity is None or character_data['rarity'].lower() == rarity:
                ids = ', '.join(map(str, character_data['ids']))
                bot.reply_to(message, f"Found {character} with rarity {character_data['rarity']} and IDs: {ids}")
            elif character_data['rarity'].lower() != rarity:
                bot.reply_to(message, f"{character} is not {rarity}. It's {character_data['rarity']}.")
    else:
        bot.reply_to(message, f"Character '{character_name}' not found.")

bot.polling()