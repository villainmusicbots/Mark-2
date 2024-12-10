from telegram.ext import CommandHandler
from datetime import datetime
from shivu import application, user_collection

# A dictionary to store cooldowns for the /pay command
pay_cooldown = {}

async def pay(update, context):
    sender_id = update.effective_user.id

    # Check if the user has replied to another message
    if not update.message.reply_to_message:
        await update.message.reply_text("Please reply to a user's message to pay!")
        return

    # Ensure the sender isn't paying themselves
    if update.message.reply_to_message.from_user.id == sender_id:
        await update.message.reply_text("You can't pay yourself!")
        return

    # Check if the sender is on cooldown for this command
    if sender_id in pay_cooldown:
        last_time = pay_cooldown[sender_id]
        if (datetime.utcnow() - last_time).total_seconds() < 60:  # 60 seconds cooldown
            await update.message.reply_text("You can only pay once every minute!")
            return

    # Retrieve the recipient's user ID and their details
    recipient_id = update.message.reply_to_message.from_user.id
    recipient_first_name = update.message.reply_to_message.from_user.first_name
    recipient_username = update.message.reply_to_message.from_user.username

    # Try to extract the amount from the command arguments
    try:
        amount = int(context.args[0])
    except (IndexError, ValueError):
        await update.message.reply_text("Invalid amount, please use /pay <amount>")
        return

    if amount <= 0:
        await update.message.reply_text("Amount must be greater than 0.")
        return

    # Check if the sender has sufficient balance
    sender_data = await user_collection.find_one({'id': sender_id})
    if not sender_data or sender_data.get('balance', 0) < amount:
        await update.message.reply_text("You don't have enough balance to complete the payment!")
        return

    # Proceed with the transaction
    await user_collection.update_one({'id': sender_id}, {'$inc': {'balance': -amount}})
    await user_collection.update_one({'id': recipient_id}, {'$inc': {'balance': amount}})

    # Update cooldown for the sender
    pay_cooldown[sender_id] = datetime.utcnow()

    # Construct the success message
    recipient_link = f"https://t.me/{recipient_username}" if recipient_username else f"https://t.me/user{recipient_id}"
    success_message = f"Success! You paid {amount} coins to {recipient_first_name}!"

    await update.message.reply_text(success_message)

# Adding the pay command handler
application.add_handler(CommandHandler('pay', pay, block=False))