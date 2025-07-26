
from telegram import Update, Bot
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from get_price_and_signal import generate_signal
import logging

# CONFIG
TOKEN = "7545012974:AAFIcvjj33l-fsQZLRMQqdyHc7EOvCyLBkc"
TELEGRAM_CHAT_ID = "6151986040"  # Your chat ID

bot = Bot(token=TOKEN)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

logger = logging.getLogger(__name__)

# SEND TRADE SIGNAL FUNCTION
def send_trade_signal(symbol, direction, entry, leverage, tp, sl, strategy, show_chart=False):
    message = (
        f"🚨 **TRADE SIGNAL** 🚨\n\n"
        f"Symbol: {symbol}\n"
        f"Direction: {direction}\n"
        f"Entry: {entry}\n"
        f"Take Profit: {tp}\n"
        f"Stop Loss: {sl}\n"
        f"Leverage: {leverage}x\n"
        f"Strategy: {strategy}"
    )
    bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message)

# COMMAND: /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Mini Bateman Bot is online and ready. Use /analyze BTC to get a trade signal."
    )

# COMMAND: /analyze
async def analyze(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args
    if not args:
        await update.message.reply_text("Usage: /analyze BTC")
        return

    symbol = args[0].upper()
    confidence, entry, tp, sl, leverage, pnl, reasoning = generate_signal(symbol)

    signal_msg = (
        f"📢 Signal by Mini Bateman | BATEMAN Method™\n"
        f"Symbol: {symbol}\n"
        f"Confidence: {confidence}%\n"
        f"Entry: {entry}\n"
        f"Take Profit: {tp}\n"
        f"Stop Loss: {sl}\n"
        f"Leverage: {leverage}x\n"
        f"PnL Potential: {pnl}%\n"
        f"Reasoning: {reasoning}"
    )
    await update.message.reply_text(signal_msg)

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("analyze", analyze))
    print("Bot started...")
    app.run_polling()

if __name__ == "__main__":
    main()
