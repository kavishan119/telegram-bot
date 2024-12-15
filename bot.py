import logging
import requests
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Hi! Send me a Zoom recording link, and I\'ll download it for you as an MP4.')

def download_zoom_recording(update: Update, context: CallbackContext) -> None:
    zoom_link = update.message.text.strip()

    if "zoom.us" not in zoom_link:
        update.message.reply_text("Please send a valid Zoom recording link.")
        return

    try:
        update.message.reply_text('Downloading the Zoom recording...')
        response = requests.get(zoom_link, stream=True)

        if response.status_code == 200:
            filename = "zoom_recording.mp4"
            with open(filename, 'wb') as file:
                for chunk in response.iter_content(chunk_size=8192):
                    file.write(chunk)

            update.message.reply_video(open(filename, 'rb'))
        else:
            update.message.reply_text("Failed to download the Zoom recording.")

    except Exception as e:
        logger.error(f"Error downloading Zoom recording: {e}")
        update.message.reply_text("An error occurred while downloading the recording.")

def main() -> None:
    updater = Updater("7337072906:AAHHEOjgRw40CJCWQfNuApEmBbtOaPmdt0E")
    updater.dispatcher.add_handler(CommandHandler("start", start))
    updater.dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, download_zoom_recording))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
