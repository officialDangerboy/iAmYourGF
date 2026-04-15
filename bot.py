import os
import requests
import logging
from dotenv import load_dotenv
from telegram import Update
from telegram.constants import ChatAction
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, filters, ContextTypes

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BOT_TOKEN = os.environ.get("BOT_TOKEN")
API_BASE  = "https://rajan-ki-ai-girlfriend-api.vercel.app/gf"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Heyy baby! 💕 Main yahan hoon tere liye!\n"
        "Kuch bhi bol, main sun rahi hoon 🥰"
    )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_msg = update.message.text

    await update.effective_chat.send_action(ChatAction.TYPING)

    try:
        res  = requests.get(API_BASE, params={"prompt": user_msg}, timeout=15)
        data = res.json()

        if data.get("status") == "success":
            reply = data.get("response", "Kuch samajh nahi aaya 😕")
        else:
            reply = "Abhi thoda busy hoon, thodi der baad baat karte hain 💕"

    except Exception as e:
        logger.error(f"API error: {e}")
        reply = "Oops! Kuch gadbad ho gayi, phir try karo 😔"

    await update.message.reply_text(reply)


if __name__ == "__main__":
    if not BOT_TOKEN:
        raise ValueError("BOT_TOKEN environment variable not set!")

    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    logger.info("Bot is running...")
    app.run_polling()
