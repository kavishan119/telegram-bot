from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import requests
import os

# Function to download video from Zoom public link
async def download_zoom_video(url, filename):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}
    response = requests.get(url, headers=headers, stream=True)

    if response.status_code == 200:
        with open(filename, 'wb') as f:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
        return filename
    else:
        return None

# Define the start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Hi! Send me a public Zoom recording link, and I will download and upload the video for you.')

# Handle messages containing Zoom links
async def handle_zoom_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message.text
    if "zoom.us/rec/play" in message:
        await update.message.reply_text("Processing your Zoom link...")
        
        # Define the output file name
        filename = "zoom_video.mp4"
        
        # Attempt to download the video
        file_path = await download_zoom_video(message, filename)

        if file_path:
            await update.message.reply_text("Download completed! Uploading the file to Telegram...")
            await update.message.reply_video(video=open(file_path, 'rb'))
            os.remove(file_path)  # Clean up the local file after sending
        else:
            await update.message.reply_text("Failed to download the video. Please ensure the link is valid and public.")
    else:
        await update.message.reply_text("This doesn't look like a valid Zoom recording link. Please send a valid public Zoom link.")

# Main function to start the bot
async def main():
    TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"  # Replace with your bot token
    application = ApplicationBuilder().token(TOKEN).build()

    # Command handlers
    application.add_handler(CommandHandler("start", start))

    # Message handler for Zoom links
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_zoom_link))

    # Start the bot
    print("Bot is running...")
    await application.run_polling()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
