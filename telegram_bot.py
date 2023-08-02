import json
import urllib.request
from telegram.ext import Updater, MessageHandler, Filters

# Replace 'YOUR_BOT_TOKEN' with your actual Telegram bot token
TOKEN = '6266214664:AAG4D4gtlnem5fWmBvQRAyJlP9EPwAtGigY'

updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher

def handle_message(update, context):
    # Get the user's first name
    user_name = update.effective_user.first_name

    # Get the received message
    message_text = update.message.text

    try:
        # Try to parse the received message as JSON
        json_data = json.loads(message_text)

        # If it's valid JSON, process the MP3 URLs and upload files
        if isinstance(json_data, dict):
            # Send a message to indicate JSON is valid and upload is starting
            context.bot.send_message(chat_id=update.effective_chat.id, text="Starting Uploads...")

            # Upload the files
            for key, mp3_url in json_data.items():
                # Upload the file with the URL as a caption
                context.bot.send_audio(chat_id=update.effective_chat.id, audio=mp3_url, caption=key)

            # Send a "completed" message
            context.bot.send_message(chat_id=update.effective_chat.id, text="Upload Completed")

        else:
            # If JSON is not a dictionary, reply with an invalid message
            context.bot.send_message(chat_id=update.effective_chat.id, text=f"Invalid")

    except json.JSONDecodeError:
        # If JSON parsing fails, reply with an invalid message
        context.bot.send_message(chat_id=update.effective_chat.id, text=f"Invalid.")

# Add the message handler to the dispatcher
message_handler = MessageHandler(Filters.text & ~Filters.command, handle_message)
dispatcher.add_handler(message_handler)

def main():
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
