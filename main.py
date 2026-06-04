import os
import logging
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from transformers import pipeline

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Load a free paraphrasing model (Hugging Face text-generation)
try:
    # Changed task name to 'text-generation' to fix the Hugging Face error
    rewriter = pipeline("text-generation", model="Vamsi/T5_Paraphrase_Paws")
except Exception as e:
    logging.error(f"Error loading model: {e}")
    rewriter = None

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a welcome message when the command /start is issued."""
    await update.message.reply_text(
        "👋 Welcome to the QuillBot Remake! \n\n"
        "Send me any sentence or paragraph, and I will rewrite/paraphrase it for you instantly."
    )

async def paraphrase_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Paraphrase the user's message."""
    user_text = update.message.text
    await update.message.reply_chat_action(action="typing")
    
    if rewriter:
        text = "paraphrase: " + user_text + " </s>"
        try:
            result = rewriter(text, max_length=256, num_return_sequences=1)
            paraphrased_text = result[0]['generated_text']
            # Clean up T5 boilerplate text if it repeats the prompt
            if "paraphrase:" in paraphrased_text:
                paraphrased_text = paraphrased_text.replace(text, "").strip()
            await update.message.reply_text(f"📝 **Rewritten:**\n\n{paraphrased_text}", parse_mode="Markdown")
        except Exception as e:
            await update.message.reply_text("⚠️ Sorry, I ran into an error trying to rewrite that.")
    else:
        await update.message.reply_text("🤖 Model is currently offline. Please try again later.")

async def main_async():
    """Async main function to support newer Python environments safely."""
    TOKEN = os.getenv("TELEGRAM_TOKEN")
    if not TOKEN:
        logging.error("No TELEGRAM_TOKEN found in environment variables!")
        return

    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, paraphrase_text))

    # Initialize and start the application lifecycle manually for safer loop management
    await application.initialize()
    await application.updater.start_polling()
    await application.start()
    
    # Keep running until the script is terminated
    while True:
        await asyncio.sleep(3600)

def main():
    # Use asyncio.run to establish the required event loop for Python 3.14+
    asyncio.run(main_async())

if __name__ == '__main__':
    main()
