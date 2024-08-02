import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from telegram import Update
import os

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

TOKEN = 'YOUR_API_TOKEN_HERE'  # Replace with your actual API token later

def start(update: Update, context: CallbackContext):
    """Send a message when the command /start is issued."""
    user_name = update.effective_user.first_name
    khmer_message = ""  # This is a Khmer message
    context.bot.send_message(chat_id=update.effective_chat.id, text=f'Hello, {user_name}! Welcome to my bot! | {khmer_message}')

def input_command(update: Update, context: CallbackContext):
    """Handle /input command."""
    if not os.path.exists('nametemp.txt'):
        context.bot.send_message(chat_id=update.effective_chat.id, text="No temporary file 'nametemp.txt' found. Creating a new one.")
        with open('nametemp.txt', 'w') as f:
            pass
    context.bot.send_message(chat_id=update.effective_chat.id, text="The next messages that you send will be inputted into a temp file. This bot only handles names in the format '(assigned name num), the name, the value'. The value which are accepted are the letter P and the letter A. Please remember the names which aren't sent are auto assigned a tick mark. Thank you for using AttendanceWriter. and to exit please use the /exit cmd")
    context.user_data['input_mode'] = True
    context.user_data['unrecorded_messages'] = []

def handle_input(update: Update, context: CallbackContext):
    """Handle input messages."""
    if context.user_data.get('input_mode'):
        message_text = update.message.text
        if message_text.startswith('/'):
            context.bot.send_message(chat_id=update.effective_chat.id, text="Invalid input. Please do not start your message with a slash.")
        else:
            with open('nametemp.txt', 'a') as f:
                f.write(message_text + '\n')
            context.bot.send_message(chat_id=update.effective_chat.id, text="Input received. Thank you!")
    else:
        context.user_data['unrecorded_messages'].append(update.message.text)
        context.bot.send_message(chat_id=update.effective_chat.id, text="Please use the /input command to start inputting data.")

def exit_command(update: Update, context: CallbackContext):
    """Handle /exit command."""
    if context.user_data.get('input_mode'):
        context.user_data['input_mode'] = False
        unrecorded_messages = context.user_data['unrecorded_messages']
        if unrecorded_messages:
            context.bot.send_message(chat_id=update.effective_chat.id, text="The following messages were not recorded:")
            for message in unrecorded_messages:
                context.bot.send_message(chat_id=update.effective_chat.id, text=message)
        else:
            context.bot.send_message(chat_id=update.effective_chat.id, text="No unrecorded messages.")
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="You are not in input mode.")

def deletetemp_command(update: Update, context: CallbackContext):
    """Handle /deletetemp command."""
    if os.path.exists('nametemp.txt'):
        os.remove('nametemp.txt')
        context.bot.send_message(chat_id=update.effective_chat.id, text="Temporary file 'nametemp.txt' deleted.")
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="No temporary file 'nametemp.txt' found.")

def error_handler(update: Update, context: CallbackContext):
    """Handle errors."""
    logging.error(f"Error: {context.error}")
    context.bot.send_message(chat_id=update.effective_chat.id, text="An error occurred. Please try again.")

def main():
    """Start the bot."""
    updater = Updater(TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Register handlers
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('input', input_command))
    dp.add_handler(CommandHandler('exit', exit_command))
    dp.add_handler(CommandHandler('deletetemp', deletetemp_command))
    dp.add_handler(MessageHandler(Filters.text, handle_input))
    dp.add_error_handler(error_handler)

    # Start the bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()