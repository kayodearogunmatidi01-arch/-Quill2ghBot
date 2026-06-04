import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from transformers import pipeline

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Load a free paraphrasing model (Hugging Face)
# Note: Render's free tier has limited RAM. If this crashes, use an external API like OpenAI or QuillBot API.
try:
    rewriter = pipeline("text2text-generation", model="Vamsi/T5_Paraphrase_Paws")
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
        # Format for the T5 paraphrase model
        text = "paraphrase: " + user_text + " </s>"
        try:
            result = rewriter(text, max_length=256, num_return_sequences=1)
            paraphrased_text = result[0]['generated_text']
            await update.message.reply_text(f"📝 **Rewritten:**\n\n{paraphrased_text}", parse_mode="Markdown")
        except Exception as e:
            await update.message.reply_text("⚠️ Sorry, I ran into an error trying to rewrite that.")
    else:
        await update.message.reply_text("🤖 Model is currently offline. Please try again later.")

def main():
    # Get token from environment variable (set this up on Render)
    TOKEN = os.getenv("TELEGRAM_TOKEN")
    
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, paraphrase_text))

    # Start the Bot
    application.run_polling()

if __name__ == '__main__':
    main()
