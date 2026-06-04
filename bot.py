import os
import logging
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Enable logging
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)

# Load tokens from environment variables (important for Render)
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends a greeting message when /start is issued."""
    await update.message.reply_text(
        "⚽ Welcome to the Sports News Bot! 🏀\n\n"
        "Use the command /news to get the latest trending sports headlines."
    )

async def get_news(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Fetches sports news and sends it to the user."""
    await update.message.reply_text("🔄 Fetching the latest sports news for you...")
    
    # Using NewsAPI as an example (Sign up for a free key at newsapi.org)
    url = f"https://newsapi.org/v2/top-headlines?category=sports&language=en&apiKey={NEWS_API_KEY}"
    
    try:
        response = requests.get(url).json()
        articles = response.get("articles", [])[:5] # Get top 5 articles
        
        if not articles:
            await update.message.reply_text("Sorry, I couldn't find any sports news right now.")
            return
            
        message_text = "🏆 *Top Sports Headlines:* \n\n"
        for article in articles:
            title = article.get("title")
            link = article.get("url")
            message_text += f"🔹 *{title}*\n🔗 [Read More]({link})\n\n"
            
        await update.message.reply_text(message_text, parse_mode="Markdown")
        
    except Exception as e:
        logging.error(f"Error fetching news: {e}")
        await update.message.reply_text("❌ Oops! Something went wrong while fetching the news.")

def main() -> None:
    """Start the bot."""
    # Build the application
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    # Register commands
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("news", get_news))

    # Run the bot using Long Polling
    application.run_polling()

if __name__ == "__main__":
    main()
