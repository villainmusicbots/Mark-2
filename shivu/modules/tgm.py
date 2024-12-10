from telegram import Update
from telegram.ext import CommandHandler, MessageHandler, Filters, CallbackContext
from shivu import application

# Command to handle /tgm
async def tgm(update: Update, context: CallbackContext) -> None:
    # Check if the user sent a photo
    if update.message.photo:
        # Get the highest quality photo from the list
        photo = update.message.photo[-1]
        
        # Get the file ID of the photo
        file = await photo.get_file()

        # Get the URL of the photo
        photo_url = file.file_url
        
        # Send the URL to the user
        await update.message.reply_text(f"Here is your photo URL: {photo_url}")
    else:
        # If no photo is sent
        await update.message.reply_text("Please send a photo to convert to a URL.")

# Add the handler for the command
application.add_handler(CommandHandler("tgm", tgm, block=False))

# Add handler for messages containing photos
application.add_handler(MessageHandler(Filters.photo, tgm, block=False))